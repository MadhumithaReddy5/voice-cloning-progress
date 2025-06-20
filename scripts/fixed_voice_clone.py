
# FIXED VERSION - Install these first:
# pip install numpy==1.24.3
# pip install torch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1

import os
import torch

def voice_clone_telugu():
    try:
        # Fix PyTorch loading
        torch.serialization.add_safe_globals([
            'TTS.tts.configs.xtts_config.XttsConfig',
            'TTS.vocoder.configs.hifigan_config.HifiganConfig'
        ])
        
        from TTS.api import TTS
        
        # Use XTTS for voice cloning
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        
        telugu_text = "అదే మరి, నీవు linear regression చూసినప్పుడు, అక్కడ మనం ఒక number predict చేయడానికి ప్రయత్నిస్తాము. దానిని regression problem అంటారు."
        
        # Voice clone with your audio
        tts.tts_to_file(
            text=telugu_text,
            speaker_wav="D:/Telugu/input/input_english.wav",
            language="te",
            file_path="D:/Telugu/output/voice_cloned_telugu.wav"
        )
        
        print("SUCCESS: Voice cloned Telugu audio created!")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    voice_clone_telugu()
