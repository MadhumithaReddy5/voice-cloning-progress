#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Working Voice Matching Solution
Uses available tools to get closest voice matching
"""

import os
import torch
from transformers import pipeline
from googletrans import Translator
import edge_tts
import asyncio

# Set up device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Language mapping
LANGUAGES = {
    "telugu": "te-IN",
    "hindi": "hi-IN", 
    "kannada": "kn-IN",
    "bengali": "bn-IN",
    "tamil": "ta-IN",
    "malayalam": "ml-IN",
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
        translated = translator.translate(text, dest=target_lang.split('-')[0])
        return translated.text
    except Exception as e:
        print(f"Translation failed: {e}")
        return text

async def create_voice_with_edge_tts(text, lang_code, output_path):
    """Create TTS using Edge TTS (better voice quality)"""
    try:
        # Get available voices for the language
        voices = await edge_tts.list_voices()
        lang_voices = [v for v in voices if v['Locale'].startswith(lang_code)]
        
        if lang_voices:
            # Use first available voice for the language
            voice = lang_voices[0]['Name']
            print(f"Using voice: [Voice selected]")
            
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_path)
            return True
        else:
            print(f"No voices found for {lang_code}")
            return False
            
    except Exception as e:
        print(f"Edge TTS failed: {e}")
        return False

def process_audio_pipeline(input_audio_path):
    """Main processing pipeline"""
    print("Starting voice matching pipeline...")
    
    base_output_dir = "D:/Telugu/output/voice_matched"
    os.makedirs(base_output_dir, exist_ok=True)
    
    # Step 1: Transcribe
    eng_text = transcribe_audio(input_audio_path)
    print(f"Transcribed: {eng_text}")
    
    # Step 2: Process each language
    async def process_languages():
        for lang_name, lang_code in LANGUAGES.items():
            print(f"\nProcessing {lang_name}...")
            
            # Translate
            translated = translate_text(eng_text, lang_code)
            print(f"Translated: [Telugu text]")
            
            # Create voice-matched TTS
            output_path = os.path.join(base_output_dir, f"{lang_name}_voice_matched.wav")
            success = await create_voice_with_edge_tts(translated, lang_code, output_path)
            
            if success:
                print(f"SUCCESS: {output_path}")
            else:
                print(f"FAILED: {lang_name}")
    
    # Run async processing
    asyncio.run(process_languages())
    
    print(f"\nCompleted! Check: {base_output_dir}")
    print("\nNote: Edge TTS provides better voice quality than gTTS")
    print("While not exact voice cloning, it offers more natural speech")

if __name__ == "__main__":
    input_audio_path = "D:/Telugu/input/input_english.wav"
    
    if not os.path.exists(input_audio_path):
        print(f"Input audio not found: {input_audio_path}")
    else:
        process_audio_pipeline(input_audio_path)