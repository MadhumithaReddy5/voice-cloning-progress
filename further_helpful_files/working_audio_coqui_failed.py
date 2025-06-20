#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Working Audio to Audio Voice Cloning
Input: English audio + manual text input
Output: Same voice in Indian languages
"""

import os
import sys
from googletrans import Translator

# Fix encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'

def clone_voice_coqui(text, lang_code, reference_audio, output_file):
    """Voice cloning using Coqui TTS"""
    try:
        from TTS.api import TTS
        import torch
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        
        tts.tts_to_file(
            text=text,
            speaker_wav=reference_audio,
            language=lang_code,
            file_path=output_file
        )
        return True
    except Exception as e:
        print(f"Coqui failed: {e}")
        return False

def main():
    print("Audio to Audio Voice Cloning")
    print("=" * 40)
    
    # Input files
    reference_audio = "D:/Telugu/input/input_english.wav"
    
    if not os.path.exists(reference_audio):
        print(f"Reference audio not found: {reference_audio}")
        print("Please place your English voice sample at the above path")
        return
    
    # Get text input (what was spoken in the audio)
    english_text = input("Enter the English text from your audio: ").strip()
    
    if not english_text:
        print("No text provided!")
        return
    
    print(f"Processing: '{english_text}'")
    
    # Languages
    languages = {
        'hindi': 'hi',
        'telugu': 'te',
        'tamil': 'ta',
        'kannada': 'kn',
        'malayalam': 'ml',
        'bengali': 'bn'
    }
    
    # Translator
    translator = Translator()
    
    # Output directory
    os.makedirs("D:/Telugu/output/voice_clones", exist_ok=True)
    
    print(f"\nCloning your voice for {len(languages)} languages...")
    
    for lang_name, lang_code in languages.items():
        print(f"\nProcessing {lang_name.title()}...")
        
        try:
            # Translate
            translated = translator.translate(english_text, dest=lang_code)
            translated_text = translated.text
            print(f"Translated: {translated_text}")
            
            # Clone voice
            output_file = f"D:/Telugu/output/voice_clones/{lang_name}_your_voice.wav"
            
            if clone_voice_coqui(translated_text, lang_code, reference_audio, output_file):
                print(f"SUCCESS: {output_file}")
            else:
                print(f"FAILED: {lang_name} (Coqui TTS not available)")
                
        except Exception as e:
            print(f"ERROR {lang_name}: {e}")
    
    print("\nCOMPLETE!")
    print("If Coqui TTS failed, install it with: pip install TTS")
    print("Or use Google Colab for better results")

if __name__ == "__main__":
    main()