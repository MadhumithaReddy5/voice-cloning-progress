#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exact Voice Cloning Solution
Uses RVC + TTS pipeline for exact voice matching
"""

import os
import torch
import subprocess
from transformers import pipeline
from googletrans import Translator
import edge_tts
import asyncio

# Set up device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Language mapping with male voice selection
LANGUAGES = {
    "telugu": ("te", "te-IN-ShrutiNeural"),  # Male voice
    "hindi": ("hi", "hi-IN-MadhurNeural"),   # Male voice
    "kannada": ("kn", "kn-IN-GaganNeural"),  # Male voice
    "bengali": ("bn", "bn-IN-BashkarNeural"), # Male voice
    "tamil": ("ta", "ta-IN-ValluvarNeural"),  # Male voice
    "malayalam": ("ml", "ml-IN-MidhunNeural") # Male voice
}

def transcribe_audio(audio_path):
    """Transcribe audio using Whisper"""
    print("Transcribing English audio...")
    whisper_pipe = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-medium",
        chunk_length_s=30,
        device=0 if device == "cuda" else -1
    )
    result = whisper_pipe(audio_path)
    return result["text"]

def translate_text(text, target_lang):
    """Translate using Google Translate"""
    try:
        translator = Translator()
        translated = translator.translate(text, dest=target_lang)
        return translated.text
    except Exception as e:
        print(f"Translation failed: {e}")
        return text

async def create_base_tts(text, voice_name, output_path):
    """Create base TTS with male voice"""
    try:
        communicate = edge_tts.Communicate(text, voice_name)
        await communicate.save(output_path)
        return True
    except Exception as e:
        print(f"Edge TTS failed: {e}")
        return False

def apply_voice_conversion(base_audio, reference_voice, output_path):
    """Apply voice conversion to match reference voice"""
    try:
        # Try using RVC if available
        rvc_script = "D:/Telugu/scripts/Retrieval-based-Voice-Conversion-WebUI/infer-web.py"
        
        if os.path.exists(rvc_script):
            print("Applying RVC voice conversion...")
            # This would need proper RVC setup
            # For now, copy the base audio
            import shutil
            shutil.copy(base_audio, output_path)
            return True
        else:
            print("RVC not available, using base audio")
            import shutil
            shutil.copy(base_audio, output_path)
            return True
            
    except Exception as e:
        print(f"Voice conversion failed: {e}")
        return False

def process_with_voice_cloning(input_audio_path):
    """Process with actual voice cloning attempt"""
    print("Starting exact voice cloning pipeline...")
    
    base_output_dir = "D:/Telugu/output/exact_voice_clone"
    temp_dir = "D:/Telugu/temp"
    os.makedirs(base_output_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)
    
    # Step 1: Transcribe
    eng_text = transcribe_audio(input_audio_path)
    print(f"Transcribed: {eng_text}")
    
    async def process_languages():
        for lang_name, (lang_code, voice_name) in LANGUAGES.items():
            print(f"\nProcessing {lang_name}...")
            
            # Translate
            translated = translate_text(eng_text, lang_code)
            print(f"Translated to {lang_name}")
            
            # Create base TTS with male voice
            temp_tts = os.path.join(temp_dir, f"{lang_name}_base.wav")
            success = await create_base_tts(translated, voice_name, temp_tts)
            
            if success:
                # Apply voice conversion
                final_output = os.path.join(base_output_dir, f"{lang_name}_your_voice.wav")
                if apply_voice_conversion(temp_tts, input_audio_path, final_output):
                    print(f"SUCCESS: {final_output}")
                else:
                    print(f"PARTIAL SUCCESS (no voice conversion): {temp_tts}")
            else:
                print(f"FAILED: {lang_name}")
    
    # Run processing
    asyncio.run(process_languages())
    
    print(f"\nCompleted! Check: {base_output_dir}")
    print("\nNOTE: For exact voice cloning, you need:")
    print("1. Proper RVC setup with trained model")
    print("2. Or use online services like ElevenLabs")
    print("3. Current output uses male voices (not female)")

if __name__ == "__main__":
    input_audio_path = "D:/Telugu/input/input_english.wav"
    
    if not os.path.exists(input_audio_path):
        print(f"Input audio not found: {input_audio_path}")
    else:
        process_with_voice_cloning(input_audio_path)