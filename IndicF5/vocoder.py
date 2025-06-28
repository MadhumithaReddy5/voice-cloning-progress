import torch
import torch.nn as nn
import numpy as np

class ResBlock(nn.Module):
    def __init__(self, channels, kernel_size=3, dilation=(1, 3, 5)):
        super().__init__()
        self.convs1 = nn.ModuleList([
            nn.Conv1d(channels, channels, kernel_size, 1, dilation=d, padding=d)
            for d in dilation
        ])
        self.convs2 = nn.ModuleList([
            nn.Conv1d(channels, channels, kernel_size, 1, dilation=1, padding=1)
            for _ in dilation
        ])
        
    def forward(self, x):
        for c1, c2 in zip(self.convs1, self.convs2):
            xt = torch.relu(x)
            xt = c1(xt)
            xt = torch.relu(xt)
            xt = c2(xt)
            x = xt + x
        return x

class HiFiGAN(nn.Module):
    def __init__(self, mel_channels=80):
        super().__init__()
        
        # Upsampling layers
        self.ups = nn.ModuleList([
            nn.ConvTranspose1d(mel_channels, 512, 16, 8, 4),
            nn.ConvTranspose1d(512, 256, 16, 8, 4),
            nn.ConvTranspose1d(256, 128, 4, 2, 1),
            nn.ConvTranspose1d(128, 64, 4, 2, 1),
        ])
        
        # Residual blocks
        self.resblocks = nn.ModuleList([
            ResBlock(512),
            ResBlock(256), 
            ResBlock(128),
            ResBlock(64),
        ])
        
        # Final conv
        self.conv_post = nn.Conv1d(64, 1, 7, 1, 3)
        
    def forward(self, x):
        # x shape: (batch, mel_channels, time)
        for up, res in zip(self.ups, self.resblocks):
            x = torch.relu(up(x))
            x = res(x)
        
        x = torch.tanh(self.conv_post(x))
        return x.squeeze(1)  # (batch, audio_length)

def load_hifigan_vocoder():
    """Load a simple HiFi-GAN style vocoder"""
    model = HiFiGAN(mel_channels=80)
    
    # Initialize with reasonable weights
    for m in model.modules():
        if isinstance(m, nn.Conv1d) or isinstance(m, nn.ConvTranspose1d):
            nn.init.kaiming_normal_(m.weight)
            if m.bias is not None:
                nn.init.zeros_(m.bias)
    
    return model

def mel_to_audio_hifigan(mel_spectrogram, sample_rate=22050):
    """Convert mel spectrogram to audio using HiFi-GAN style vocoder"""
    
    # Load vocoder
    vocoder = load_hifigan_vocoder()
    vocoder.eval()
    
    # Prepare input
    if len(mel_spectrogram.shape) == 2:
        mel_spectrogram = mel_spectrogram[None, ...]  # Add batch dim
    
    mel_tensor = torch.FloatTensor(mel_spectrogram)
    
    # Generate audio
    with torch.no_grad():
        audio = vocoder(mel_tensor)
    
    # Convert to numpy
    audio = audio.squeeze().cpu().numpy()
    
    # Normalize
    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio)) * 0.8
    
    return audio