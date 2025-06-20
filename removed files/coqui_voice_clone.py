
import os
import torch
from TTS.api import TTS

def clone_voice_with_coqui():
    """Clone voice using Coqui XTTS"""
    
    try:
        # Fix PyTorch loading issues
        torch.serialization.add_safe_globals([
            'TTS.tts.configs.xtts_config.XttsConfig',
            'TTS.vocoder.configs.hifigan_config.HifiganConfig',
            'TTS.tts.layers.xtts.tokenizer.VoiceBpeTokenizer'
        ])
        
        # Load XTTS model
        print("Loading Coqui XTTS model...")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
        
        # Method 1: Try Telugu directly (might work with phonetic spelling)
        telugu_phonetic = "Ade mari, neevu linear regression choosinappudu, akkada manam oka number predict cheyadaniki prayatnistamu. Danini regression problem antaru."
        
        print("Attempting Telugu voice cloning...")
        tts.tts_to_file(
            text=telugu_phonetic,
            speaker_wav="D:/Telugu/input/input_english.wav",
            language="en",  # Use English language model
            file_path="D:/Telugu/output/coqui_telugu_attempt1.wav"
        )
        
        # Method 2: Generate in Hindi (closer to Telugu phonetically)
        hindi_text = "दूसरी ओर, जब आपने linear regression देखा है, वहाँ हम एक number predict करने की कोशिश करते हैं। इसे regression problem कहते हैं।"
        
        print("Generating in Hindi for better phonetics...")
        tts.tts_to_file(
            text=hindi_text,
            speaker_wav="D:/Telugu/input/input_english.wav",
            language="hi",
            file_path="D:/Telugu/output/coqui_hindi_version.wav"
        )
        
        # Method 3: English with Telugu pronunciation
        english_telugu_mix = "Ade mari, when you have seen the linear regression, akkada we try to predict a number. Danini regression problem antaru."
        
        print("Generating English-Telugu mix...")
        tts.tts_to_file(
            text=english_telugu_mix,
            speaker_wav="D:/Telugu/input/input_english.wav",
            language="en",
            file_path="D:/Telugu/output/coqui_english_telugu_mix.wav"
        )
        
        print("SUCCESS: Multiple versions created!")
        print("Files created:")
        print("1. coqui_telugu_attempt1.wav - Direct Telugu attempt")
        print("2. coqui_hindi_version.wav - Hindi version (similar phonetics)")
        print("3. coqui_english_telugu_mix.wav - Mixed approach")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nTroubleshooting:")
        print("1. Install correct versions: pip install numpy==1.24.3 torch==1.13.1")
        print("2. Try running as administrator")
        print("3. Clear pip cache: pip cache purge")
        return False

if __name__ == "__main__":
    clone_voice_with_coqui()
