import os
import torch
import torch.nn as nn
import json
import librosa
import soundfile as sf
import pandas as pd
import numpy as np
import logging
import time
from datetime import datetime
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence

# Setup logging
def setup_logging():
    os.makedirs('logs', exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f'logs/training_{timestamp}.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

class TeluguDataset(Dataset):
    def __init__(self, metadata_path, audio_dir, sample_rate=22050, max_audio_length=10, limit_samples=None):
        self.metadata = pd.read_csv(metadata_path)
        if limit_samples is not None:
            self.metadata = self.metadata.head(limit_samples)
        self.audio_dir = audio_dir
        self.sample_rate = sample_rate
        self.max_audio_length = max_audio_length
        
        # Telugu character mapping
        self.char_to_idx = self.create_char_mapping()
        
    def create_char_mapping(self):
        """Create character to index mapping for Telugu"""
        telugu_chars = "అఆఇఈఉఊఋౠఎఏఐఒఓఔకఖగఘఙచఛజఝఞటఠడఢణతథదధనపఫబభమయరఱలళవశషసహౘౙ౛ాిీుూృౄెేైొోౌ్ౕౖంఁఃౢౣ"
        english_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        numbers = "0123456789"
        punctuation = ".,!?-—\"'():; "
        
        all_chars = telugu_chars + english_chars + numbers + punctuation
        char_to_idx = {char: idx + 1 for idx, char in enumerate(all_chars)}  # +1 for padding
        char_to_idx['<PAD>'] = 0
        char_to_idx['<UNK>'] = len(char_to_idx)
        
        return char_to_idx
        
    def text_to_sequence(self, text):
        """Convert text to sequence of indices"""
        return [self.char_to_idx.get(char, self.char_to_idx['<UNK>']) for char in text]
        
    def __len__(self):
        return len(self.metadata)
    
    def __getitem__(self, idx):
        row = self.metadata.iloc[idx]
        audio_file = row['audio_file'] if 'audio_file' in row else row.iloc[0]
        text = row['text'] if 'text' in row else row.iloc[1]
        
        # Fix path issue - remove extra 'wavs/' prefix if present
        if audio_file.startswith('wavs/'):
            audio_file = audio_file[5:]
        audio_path = os.path.join(self.audio_dir, audio_file)
        
        try:
            # Load audio
            audio, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # Trim or pad audio to max length
            max_samples = int(self.max_audio_length * self.sample_rate)
            if len(audio) > max_samples:
                audio = audio[:max_samples]
            else:
                audio = np.pad(audio, (0, max_samples - len(audio)))
            
            # Convert to mel spectrogram
            mel = librosa.feature.melspectrogram(
                y=audio, sr=sr, n_mels=80, hop_length=256, win_length=1024,
                fmin=0, fmax=8000
            )
            mel = librosa.power_to_db(mel, ref=np.max)
            
            # Normalize mel spectrogram
            mel = (mel + 80) / 80  # Rough normalization
            
            # Convert text to sequence
            text_seq = self.text_to_sequence(text)
            
            return {
                'text': torch.LongTensor(text_seq),
                'mel': torch.FloatTensor(mel),
                'audio': torch.FloatTensor(audio),
                'text_length': len(text_seq),
                'mel_length': mel.shape[1]
            }
        except Exception as e:
            print(f"Error loading {audio_path}: {e}")
            # Return dummy data
            return {
                'text': torch.LongTensor([1]),
                'mel': torch.FloatTensor(np.zeros((80, 100))),
                'audio': torch.FloatTensor(np.zeros(22050)),
                'text_length': 1,
                'mel_length': 100
            }

def collate_fn(batch):
    """Custom collate function for batching"""
    texts = [item['text'] for item in batch]
    mels = [item['mel'].transpose(0, 1) for item in batch]  # (time, mel_dim)
    audios = [item['audio'] for item in batch]
    text_lengths = [item['text_length'] for item in batch]
    mel_lengths = [item['mel_length'] for item in batch]
    
    # Pad sequences
    texts_padded = pad_sequence(texts, batch_first=True, padding_value=0)
    mels_padded = pad_sequence(mels, batch_first=True, padding_value=0)
    audios_padded = pad_sequence(audios, batch_first=True, padding_value=0)
    
    return {
        'texts': texts_padded,
        'mels': mels_padded.transpose(1, 2),  # Back to (batch, mel_dim, time)
        'audios': audios_padded,
        'text_lengths': torch.LongTensor(text_lengths),
        'mel_lengths': torch.LongTensor(mel_lengths)
    }

class IndicF5Model(nn.Module):
    def __init__(self, vocab_size, d_model=512, n_heads=8, n_layers=6):
        super().__init__()
        self.d_model = d_model
        
        # Text encoder
        self.text_embedding = nn.Embedding(vocab_size, d_model)
        self.text_pos_encoding = nn.Parameter(torch.randn(1000, d_model))
        
        # Transformer encoder for text
        encoder_layer = nn.TransformerEncoderLayer(d_model, n_heads, batch_first=True)
        self.text_encoder = nn.TransformerEncoder(encoder_layer, n_layers)
        
        # Decoder for mel generation
        decoder_layer = nn.TransformerDecoderLayer(d_model, n_heads, batch_first=True)
        self.mel_decoder = nn.TransformerDecoder(decoder_layer, n_layers)
        
        # Mel projection
        self.mel_projection = nn.Linear(d_model, 80)
        self.mel_input_projection = nn.Linear(80, d_model)
        
        # Duration predictor
        self.duration_predictor = nn.Sequential(
            nn.Linear(d_model, 256),
            nn.ReLU(),
            nn.Linear(256, 1)
        )
        
    def forward(self, texts, text_lengths, mels=None, mel_lengths=None):
        batch_size, text_len = texts.shape
        
        # Text encoding
        text_emb = self.text_embedding(texts)
        text_emb += self.text_pos_encoding[:text_len].unsqueeze(0)
        
        # Create text mask
        text_mask = torch.zeros(batch_size, text_len, dtype=torch.bool, device=texts.device)
        for i, length in enumerate(text_lengths):
            text_mask[i, length:] = True
        
        # Encode text
        text_encoded = self.text_encoder(text_emb, src_key_padding_mask=text_mask)
        
        # Predict durations
        durations = self.duration_predictor(text_encoded).squeeze(-1)
        durations = torch.relu(durations)
        
        if mels is not None:
            # Training mode
            mel_len = mels.shape[2]
            
            # Create mel input (shifted right)
            mel_input = torch.zeros(batch_size, 80, mel_len, device=mels.device)
            mel_input[:, :, 1:] = mels[:, :, :-1]
            mel_input = mel_input.transpose(1, 2)  # (batch, time, mel_dim)
            mel_input = self.mel_input_projection(mel_input)  # Project to d_model
            
            # Decode
            mel_output = self.mel_decoder(
                mel_input,
                text_encoded,
                tgt_key_padding_mask=None,
                memory_key_padding_mask=text_mask
            )
            
            mel_pred = self.mel_projection(mel_output).transpose(1, 2)  # (batch, mel_dim, time)
            
            return mel_pred, durations
        else:
            # Inference mode - use duration-based expansion
            durations_int = torch.clamp(torch.round(durations * 10), min=1).long()
            
            # Expand text features based on durations
            expanded_features = []
            for b in range(batch_size):
                text_len = text_lengths[b]
                expanded = []
                for t in range(text_len):
                    dur = durations_int[b, t].item()
                    expanded.extend([text_encoded[b, t]] * dur)
                if expanded:
                    expanded_features.append(torch.stack(expanded))
                else:
                    expanded_features.append(text_encoded[b, :1])  # Fallback
            
            # Pad to same length
            max_len = max(len(feat) for feat in expanded_features)
            mel_features = torch.zeros(batch_size, max_len, self.d_model, device=texts.device)
            for b, feat in enumerate(expanded_features):
                mel_features[b, :len(feat)] = feat
            
            mel_pred = self.mel_projection(mel_features).transpose(1, 2)
            return mel_pred, durations

def train_indicf5():
    """Main training function"""
    # Load config
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    print(f"Training IndicF5 for Telugu TTS")
    print(f"Dataset: {config['dataset_path']}")
    
    # Create dataset with limited samples for testing
    dataset = TeluguDataset(
        metadata_path=os.path.join(config['dataset_path'], 'metadata_with_speakers.csv'),
        audio_dir=os.path.join(config['dataset_path'], 'wavs'),
        sample_rate=config['sample_rate'],
        limit_samples=config.get('limit_samples', None)
    )
    
    print(f"Dataset size: {len(dataset)} samples")
    
    dataloader = DataLoader(
        dataset, 
        batch_size=config['batch_size'], 
        shuffle=True,
        collate_fn=collate_fn,
        num_workers=0
    )
    
    # Initialize model
    vocab_size = len(dataset.char_to_idx)
    model = IndicF5Model(vocab_size=vocab_size)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    
    # Optimizer and loss
    optimizer = torch.optim.Adam(model.parameters(), lr=config.get('learning_rate', 1e-4))
    criterion = nn.MSELoss()
    
    print(f"Model initialized with {sum(p.numel() for p in model.parameters())} parameters")
    print(f"Training on device: {device}")
    
    # Create directories
    os.makedirs('checkpoints', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    
    # Training loop
    model.train()
    print(f"Starting training for {config.get('epochs', 10)} epochs...")
    
    for epoch in range(config.get('epochs', 10)):
        print(f"Starting epoch {epoch+1}")
        total_loss = 0
        
        print(f"DataLoader has {len(dataloader)} batches")
        for batch_idx, batch in enumerate(dataloader):
            try:
                print(f"Processing batch {batch_idx}")
                texts = batch['texts'].to(device)
                mels = batch['mels'].to(device)
                text_lengths = batch['text_lengths'].to(device)
                mel_lengths = batch['mel_lengths'].to(device)
                
                print(f"Batch shapes - texts: {texts.shape}, mels: {mels.shape}")
                
                optimizer.zero_grad()
                
                mel_pred, durations = model(texts, text_lengths, mels, mel_lengths)
                
                # Calculate loss
                loss = criterion(mel_pred, mels)
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
                
                if batch_idx % 5 == 0:
                    print(f"Epoch {epoch+1}, Batch {batch_idx}, Loss: {loss.item():.4f}")
                    
            except Exception as e:
                print(f"Error in batch {batch_idx}: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        avg_loss = total_loss / len(dataloader)
        print(f"Epoch {epoch+1} completed. Average Loss: {avg_loss:.4f}")
        
        # Save checkpoint
        if epoch % config.get('save_every', 5) == 0:
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': avg_loss,
                'char_to_idx': dataset.char_to_idx,
            }, f'checkpoints/checkpoint_epoch_{epoch}.pth')
    
    print("Training completed!")

if __name__ == "__main__":
    try:
        train_indicf5()
    except Exception as e:
        print(f"Training failed with error: {e}")
        import traceback
        traceback.print_exc()