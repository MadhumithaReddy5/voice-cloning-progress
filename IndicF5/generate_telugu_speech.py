import torch
import json
import librosa
import soundfile as sf
import numpy as np
from train_indicf5_telugu import IndicF5Model

def generate_telugu_speech(text, checkpoint_path, config_path, output_path):
    """Generate Telugu speech from text"""
    
    # Use text directly (should be Telugu)
    telugu_text = text
    
    # Load config
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Load checkpoint
    checkpoint = torch.load(checkpoint_path, map_location='cpu')
    char_to_idx = checkpoint['char_to_idx']
    
    # Initialize model
    vocab_size = len(char_to_idx)
    model = IndicF5Model(vocab_size=vocab_size)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    
    print(f"Loaded model from epoch {checkpoint['epoch']}")
    print(f"Using device: {device}")
    
    # Convert text to sequence
    def text_to_sequence(text, char_to_idx):
        return [char_to_idx.get(char, char_to_idx['<UNK>']) for char in text]
    
    text_seq = text_to_sequence(telugu_text, char_to_idx)
    text_tensor = torch.LongTensor(text_seq).unsqueeze(0).to(device)
    text_length = torch.LongTensor([len(text_seq)]).to(device)
    
    print(f"Input text: {telugu_text}")
    print(f"Text sequence length: {len(text_seq)}")
    
    # Generate mel spectrogram
    with torch.no_grad():
        mel_output, durations = model(text_tensor, text_length)
    
    # Convert to numpy
    mel_np = mel_output.squeeze().cpu().numpy()
    
    print(f"Generated mel shape: {mel_np.shape}")
    
    # Force longer mel sequence if too short
    if mel_np.shape[1] < 50:  # If less than 50 frames (~0.6 seconds)
        print("Mel sequence too short, extending...")
        # Repeat the mel sequence to make it longer
        repeat_factor = max(3, 50 // mel_np.shape[1])
        mel_np = np.tile(mel_np, (1, repeat_factor))
        print(f"Extended mel shape: {mel_np.shape}")
    
    # Properly denormalize mel spectrogram
    mel_np = mel_np * 4.0  # Scale factor for mel
    
    # Convert mel to audio using inverse mel transformation
    try:
        # Use librosa's inverse mel transformation
        audio = librosa.feature.inverse.mel_to_audio(
            mel_np,
            sr=config['sample_rate'],
            n_fft=config['win_length'],
            hop_length=config['hop_length'],
            win_length=config['win_length'],
            fmin=config['mel_fmin'],
            fmax=config['mel_fmax'],
            n_iter=32
        )
        
        # Normalize audio
        if np.max(np.abs(audio)) > 0:
            audio = audio / np.max(np.abs(audio)) * 0.7
        
        # Save audio
        sf.write(output_path, audio, config['sample_rate'])
        print(f"Generated Telugu audio saved to: {output_path}")
        print(f"Audio duration: {len(audio)/config['sample_rate']:.2f} seconds")
        
        return audio
        
    except Exception as e:
        print(f"Error converting mel to audio: {e}")
        # Fallback: save mel as image for debugging
        import matplotlib.pyplot as plt
        plt.figure(figsize=(12, 4))
        plt.imshow(mel_np, aspect='auto', origin='lower')
        plt.title('Generated Mel Spectrogram')
        plt.colorbar()
        mel_image_path = output_path.replace('.wav', '_mel.png')
        plt.savefig(mel_image_path)
        print(f"Saved mel spectrogram image to: {mel_image_path}")
        return None

def interactive_generation():
    """Interactive Telugu speech generation"""
    config_path = "config.json"
    
    # Find latest checkpoint
    import os
    checkpoint_dir = "checkpoints"
    if not os.path.exists(checkpoint_dir):
        print("No checkpoints found. Please train the model first.")
        return
    
    checkpoints = [f for f in os.listdir(checkpoint_dir) if f.endswith('.pth')]
    if not checkpoints:
        print("No checkpoint files found. Please train the model first.")
        return
    
    # Get latest checkpoint
    latest_checkpoint = sorted(checkpoints)[-1]
    checkpoint_path = os.path.join(checkpoint_dir, latest_checkpoint)
    
    print(f"Using checkpoint: {checkpoint_path}")
    
    while True:
        print("\n" + "="*50)
        print("Telugu TTS - IndicF5")
        print("="*50)
        
        text = input("Enter Telugu text (or 'quit' to exit): ").strip()
        
        if text.lower() == 'quit':
            break
        
        if not text:
            continue
        
        # Generate filename
        import time
        timestamp = int(time.time())
        output_path = f"outputs/telugu_output_{timestamp}.wav"
        
        try:
            audio = generate_telugu_speech(text, checkpoint_path, config_path, output_path)
            if audio is not None:
                print(f"✓ Audio generated successfully!")
                
                # Option to play audio (if available)
                try:
                    import pygame
                    pygame.mixer.init()
                    pygame.mixer.music.load(output_path)
                    play = input("Play audio? (y/n): ").strip().lower()
                    if play == 'y':
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy():
                            pygame.time.wait(100)
                except ImportError:
                    print("Install pygame to play audio: pip install pygame")
                except Exception as e:
                    print(f"Could not play audio: {e}")
            
        except Exception as e:
            print(f"Error generating speech: {e}")

if __name__ == "__main__":
    # Example usage
    sample_texts = [
        "నమస్కారం",
        "ఇది తెలుగు టెక్స్ట్ టు స్పీచ్ సిస్టమ్",
        "మీరు ఎలా ఉన్నారు?",
        "Hello, this is a test."
    ]
    
    print("Sample Telugu texts for testing:")
    for i, text in enumerate(sample_texts, 1):
        print(f"{i}. {text}")
    
    print("\nStarting interactive generation...")
    interactive_generation()