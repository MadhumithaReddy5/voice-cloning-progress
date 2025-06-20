
# WORKING COQUI VOICE CLONE SCRIPT
# Run after fixing environment

import torch
import os

def clone_voice_exact():
    try:
        # Fix PyTorch loading
        torch.serialization.add_safe_globals([
            'TTS.tts.configs.xtts_config.XttsConfig'
        ])
        
        from TTS.api import TTS
        
        # Load XTTS for voice cloning
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        
        # Telugu text
        telugu_text = "అదే మరి, నీవు లినియర్ రిగ్రెషన్ చూసినప్పుడు, అక్కడ మనం ఒక నంబర్ ప్రిడిక్ట్ చేయడానికి ప్రయత్నిస్తాము. దానిని రిగ్రెషన్ ప్రాబ్లెమ్ అంటారు."
        
        # Clone your voice
        tts.tts_to_file(
            text=telugu_text,
            speaker_wav="D:/Telugu/input/input_english.wav",
            language="te",
            file_path="D:/Telugu/output/exact_voice_telugu.wav"
        )
        
        print("SUCCESS: Exact voice Telugu created!")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Use ElevenLabs instead")

if __name__ == "__main__":
    clone_voice_exact()
