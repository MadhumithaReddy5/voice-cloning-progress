import numpy as np
import soundfile as sf
from scipy.signal import butter, filtfilt, hilbert
import librosa

def advanced_mel_to_audio(mel_spectrogram, sample_rate=22050, hop_length=256):
    """Advanced mel to audio conversion using multiple techniques"""
    
    mel_np = mel_spectrogram.astype(np.float32)
    
    # Method 1: Harmonic + Noise synthesis
    audio_length = mel_np.shape[1] * hop_length
    audio = np.zeros(audio_length)
    
    # Generate harmonic content
    for frame_idx in range(mel_np.shape[1]):
        start_sample = frame_idx * hop_length
        end_sample = min(start_sample + hop_length, len(audio))
        
        if end_sample > start_sample:
            mel_frame = mel_np[:, frame_idx]
            
            # Find dominant frequencies
            dominant_bins = np.argsort(mel_frame)[-8:]  # Top 8 bins
            
            frame_audio = np.zeros(end_sample - start_sample)
            t = np.linspace(0, hop_length/sample_rate, end_sample - start_sample)
            
            # Generate harmonics
            for i, bin_idx in enumerate(dominant_bins):
                freq = 80 + (bin_idx / 80.0) * 3920  # Map to frequency
                amplitude = mel_frame[bin_idx] * 0.05
                
                # Add fundamental and harmonics
                frame_audio += amplitude * np.sin(2 * np.pi * freq * t)
                if freq * 2 < 4000:
                    frame_audio += amplitude * 0.5 * np.sin(2 * np.pi * freq * 2 * t)
                if freq * 3 < 4000:
                    frame_audio += amplitude * 0.25 * np.sin(2 * np.pi * freq * 3 * t)
            
            audio[start_sample:end_sample] += frame_audio
    
    # Method 2: Add noise component for naturalness
    noise = np.random.randn(len(audio)) * 0.05
    
    # Filter noise based on mel energy
    for frame_idx in range(mel_np.shape[1]):
        start_sample = frame_idx * hop_length
        end_sample = min(start_sample + hop_length, len(audio))
        
        if end_sample > start_sample:
            mel_energy = np.mean(mel_np[:, frame_idx])
            noise[start_sample:end_sample] *= mel_energy
    
    audio += noise
    
    # Method 3: Apply formant filtering
    # Create multiple formant filters
    formant_freqs = [500, 1500, 2500]  # Typical speech formants
    
    for freq in formant_freqs:
        # Create bandpass filter around formant
        low_freq = max(freq - 200, 100)
        high_freq = min(freq + 200, sample_rate//2 - 100)
        
        b, a = butter(2, [low_freq, high_freq], btype='band', fs=sample_rate)
        formant_component = filtfilt(b, a, audio)
        audio += formant_component * 0.3
    
    # Method 4: Apply spectral envelope
    # Use Hilbert transform for envelope shaping
    analytic_signal = hilbert(audio)
    amplitude_envelope = np.abs(analytic_signal)
    
    # Smooth the envelope
    from scipy.ndimage import gaussian_filter1d
    smooth_envelope = gaussian_filter1d(amplitude_envelope, sigma=100)
    
    # Apply envelope modulation
    if np.max(smooth_envelope) > 0:
        audio = audio * (smooth_envelope / np.max(smooth_envelope))
    
    # Method 5: Final processing
    # Apply speech-like filtering
    b, a = butter(4, [200, 4000], btype='band', fs=sample_rate)
    audio = filtfilt(b, a, audio)
    
    # Dynamic range compression (like human speech)
    audio = np.tanh(audio * 2) * 0.5
    
    # Normalize
    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio)) * 0.8
    
    return audio

def test_improved_vocoder():
    """Test the improved vocoder with your model"""
    from generate_telugu_speech import generate_telugu_speech
    
    # Generate using your model but with improved vocoder
    # You'll need to modify generate_telugu_speech.py to use this function
    
    print("Testing improved vocoder...")
    # This is a placeholder - integrate with your existing model
    
if __name__ == "__main__":
    test_improved_vocoder()