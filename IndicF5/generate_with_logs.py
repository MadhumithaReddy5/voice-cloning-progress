import torch
import json
import librosa
import soundfile as sf
import numpy as np
import logging
import time
from datetime import datetime
from train_with_logs import IndicF5Model
from googletrans import Translator

# Setup logging for inference
def setup_inference_logging():
    os.makedirs('logs', exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f'logs/inference_{timestamp}.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def generate_telugu_speech(text, checkpoint_path, config_path, output_path, logger=None):
    """Generate Telugu speech from text with logging"""
    
    if logger is None:
        logger = logging.getLogger(__name__)
    
    start_time = time.time()
    logger.info(f"Starting speech generation for: '{text}'")
    
    # Translate English to Telugu if needed
    translator = Translator()
    try:
        detected = translator.detect(text)
        if detected.lang == 'en':
            translated = translator.translate(text, src='en', dest='te')
            telugu_text = translated.text
            logger.info(f"Translated '{text}' to '{telugu_text}'")
        else:
            telugu_text = text
            logger.info(f"Input already in Telugu: '{telugu_text}'")
    except Exception as e:
        logger.warning(f"Translation failed: {e}, using original text")
        telugu_text = text
    
    # Load config
    with open(config_path, 'r') as f:
        config = json.load(f)
    logger.info(f"Loaded config from {config_path}")
    
    # Load checkpoint
    logger.info(f"Loading checkpoint from {checkpoint_path}")
    checkpoint = torch.load(checkpoint_path, map_location='cpu')
    char_to_idx = checkpoint['char_to_idx']
    
    # Initialize model
    vocab_size = len(char_to_idx)
    model = IndicF5Model(vocab_size=vocab_size)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    
    logger.info(f"Model loaded from epoch {checkpoint['epoch']}")
    logger.info(f"Using device: {device}")
    logger.info(f"Vocabulary size: {vocab_size}")
    
    # Convert text to sequence
    def text_to_sequence(text, char_to_idx):
        return [char_to_idx.get(char, char_to_idx['<UNK>']) for char in text]
    
    text_seq = text_to_sequence(telugu_text, char_to_idx)
    text_tensor = torch.LongTensor(text_seq).unsqueeze(0).to(device)
    text_length = torch.LongTensor([len(text_seq)]).to(device)
    
    logger.info(f"Text sequence length: {len(text_seq)}")
    logger.info(f"Text tensor shape: {text_tensor.shape}")
    
    # Generate mel spectrogram
    logger.info("Generating mel spectrogram...")
    generation_start = time.time()
    
    with torch.no_grad():
        mel_output, durations = model(text_tensor, text_length)
    
    generation_time = time.time() - generation_start
    logger.info(f"Mel generation completed in {generation_time:.2f}s")
    
    # Convert to numpy
    mel_np = mel_output.squeeze().cpu().numpy()
    logger.info(f"Generated mel shape: {mel_np.shape}")
    
    # Force longer mel sequence if too short
    if mel_np.shape[1] < 50:
        logger.warning("Mel sequence too short, extending...")
        repeat_factor = max(3, 50 // mel_np.shape[1])
        mel_np = np.tile(mel_np, (1, repeat_factor))
        logger.info(f"Extended mel shape: {mel_np.shape}")
    
    # Denormalize mel spectrogram  
    mel_np = (mel_np * 80) - 80
    logger.info("Mel spectrogram denormalized")
    
    # Convert mel to audio
    logger.info("Converting mel to audio...")
    audio_start = time.time()
    
    try:
        mel_np = mel_np.astype(np.float32)
        
        # Create audio duration based on mel frames
        audio_duration = max(3.0, mel_np.shape[1] * config['hop_length'] / config['sample_rate'])
        audio_length = int(audio_duration * config['sample_rate'])
        
        logger.info(f"Target audio duration: {audio_duration:.2f}s ({audio_length} samples)")
        
        # Generate audio using additive synthesis
        t = np.linspace(0, audio_duration, audio_length)
        audio = np.zeros(audio_length)
        
        # For each mel frame, generate corresponding audio
        for frame_idx in range(mel_np.shape[1]):
            frame_start = int(frame_idx * config['hop_length'] / config['sample_rate'] * config['sample_rate'])
            frame_end = min(frame_start + config['hop_length'], audio_length)
            
            if frame_end > frame_start:
                # Use mel bins to create harmonic content
                mel_frame = mel_np[:, frame_idx]
                
                # Find prominent frequency bins
                prominent_bins = np.argsort(mel_frame)[-10:]  # Top 10 bins
                
                frame_audio = np.zeros(frame_end - frame_start)
                frame_t = t[frame_start:frame_end]
                
                for bin_idx in prominent_bins:
                    # Map mel bin to frequency (rough approximation)
                    freq = 80 + (bin_idx / 80.0) * 3920  # 80Hz to 4000Hz
                    amplitude = mel_frame[bin_idx] * 0.1
                    
                    # Add sine wave component
                    frame_audio += amplitude * np.sin(2 * np.pi * freq * frame_t)
                    
                    # Add some harmonics
                    if freq * 2 < 4000:
                        frame_audio += amplitude * 0.3 * np.sin(2 * np.pi * freq * 2 * frame_t)
                
                audio[frame_start:frame_end] += frame_audio
        
        # Apply envelope to make it more speech-like
        envelope = np.abs(audio)
        envelope = np.convolve(envelope, np.ones(1000)/1000, mode='same')  # Smooth envelope
        audio = audio * (envelope + 0.1)
        
        # Normalize
        if np.max(np.abs(audio)) > 0:
            audio = audio / np.max(np.abs(audio)) * 0.6
        
        # Apply fade in/out
        fade_samples = int(0.1 * config['sample_rate'])
        audio[:fade_samples] *= np.linspace(0, 1, fade_samples)
        audio[-fade_samples:] *= np.linspace(1, 0, fade_samples)
        
        audio_time = time.time() - audio_start
        logger.info(f"Audio conversion completed in {audio_time:.2f}s")
        
        # Save audio
        sf.write(output_path, audio, config['sample_rate'])
        
        total_time = time.time() - start_time
        logger.info(f"Generated Telugu audio saved to: {output_path}")
        logger.info(f"Audio duration: {len(audio)/config['sample_rate']:.2f} seconds")
        logger.info(f"Total generation time: {total_time:.2f}s")
        
        return audio
        
    except Exception as e:
        logger.error(f"Error converting mel to audio: {e}")
        import traceback
        logger.error(traceback.format_exc())
        
        # Fallback: save mel as image for debugging
        try:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(12, 4))
            plt.imshow(mel_np, aspect='auto', origin='lower')
            plt.title('Generated Mel Spectrogram')
            plt.colorbar()
            mel_image_path = output_path.replace('.wav', '_mel.png')
            plt.savefig(mel_image_path)
            logger.info(f"Saved mel spectrogram image to: {mel_image_path}")
        except Exception as plot_e:
            logger.error(f"Could not save mel image: {plot_e}")
        
        return None

def interactive_generation():
    """Interactive Telugu speech generation with logging"""
    logger = setup_inference_logging()
    config_path = "config.json"
    
    logger.info("=" * 60)
    logger.info("STARTING INTERACTIVE TELUGU TTS GENERATION")
    logger.info("=" * 60)
    
    # Find latest checkpoint
    import os
    checkpoint_dir = "checkpoints"
    if not os.path.exists(checkpoint_dir):
        logger.error("No checkpoints found. Please train the model first.")
        return
    
    checkpoints = [f for f in os.listdir(checkpoint_dir) if f.endswith('.pth')]
    if not checkpoints:
        logger.error("No checkpoint files found. Please train the model first.")
        return
    
    # Get latest checkpoint
    latest_checkpoint = sorted(checkpoints)[-1]
    checkpoint_path = os.path.join(checkpoint_dir, latest_checkpoint)
    
    logger.info(f"Using checkpoint: {checkpoint_path}")
    
    while True:
        print("\n" + "="*50)
        print("Telugu TTS - IndicF5")
        print("="*50)
        
        text = input("Enter English/Telugu text (or 'quit' to exit): ").strip()
        
        if text.lower() == 'quit':
            logger.info("User requested exit")
            break
        
        if not text:
            continue
        
        # Generate filename
        timestamp = int(time.time())
        output_path = f"outputs/telugu_output_{timestamp}.wav"
        
        try:
            audio = generate_telugu_speech(text, checkpoint_path, config_path, output_path, logger)
            if audio is not None:
                print(f"✓ Audio generated successfully!")
                logger.info("Audio generation successful")
                
                # Option to play audio (if available)
                try:
                    import pygame
                    pygame.mixer.init()
                    pygame.mixer.music.load(output_path)
                    play = input("Play audio? (y/n): ").strip().lower()
                    if play == 'y':
                        pygame.mixer.music.play()
                        logger.info("Playing generated audio")
                        while pygame.mixer.music.get_busy():
                            pygame.time.wait(100)
                except ImportError:
                    logger.warning("pygame not available for audio playback")
                    print("Install pygame to play audio: pip install pygame")
                except Exception as e:
                    logger.error(f"Could not play audio: {e}")
            else:
                logger.error("Audio generation failed")
            
        except Exception as e:
            logger.error(f"Error generating speech: {e}")
            import traceback
            logger.error(traceback.format_exc())

if __name__ == "__main__":
    import os
    
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