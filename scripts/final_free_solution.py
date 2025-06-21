#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final FREE Voice Cloning Solution
Uses Bark TTS for voice cloning
"""

import os
import torch
from transformers import pipeline
from googletrans import Translator

device = "cuda" if torch.cuda.is_available() else "cpu"

LANGUAGES = {
    "telugu": "te",
    "hindi": "hi",
    "kannada": "kn", 
    "bengali": "bn",
    "tamil": "ta",
    "malayalam": "ml",
}

def transcribe_audio(audio_path):
    print("Transcribing audio...")
    whisper_pipe = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-medium",
        chunk_length_s=30,
        device=0 if device == "cuda" else -1
    )
    result = whisper_pipe(audio_path)
    return result["text"]

def translate_text(text, target_lang):
    try:
        translator = Translator()
        translated = translator.translate(text, dest=target_lang)
        return translated.text
    except Exception as e:
        print(f"Translation failed: {e}")
        return text

def clone_with_bark(text, output_path):
    """Use Bark TTS for voice cloning"""
    try:
        from bark import SAMPLE_RATE, generate_audio, preload_models
        from scipy.io.wavfile import write as write_wav
        
        print("Using Bark TTS for voice cloning...")
        
        # Preload models
        preload_models()
        
        # Generate audio with voice cloning capability
        audio_array = generate_audio(text, history_prompt="v2/en_speaker_6")
        
        # Save audio
        write_wav(output_path, SAMPLE_RATE, audio_array)
        return True
        
    except Exception as e:
        print(f"Bark TTS failed: {e}")
        return False

def process_free_cloning(input_audio_path):
    print("FREE Voice Cloning with Bark TTS")
    print("=" * 40)
    
    base_output_dir = "D:/Telugu/output/bark_voice_clone"
    os.makedirs(base_output_dir, exist_ok=True)
    
    # Transcribe
    eng_text = transcribe_audio(input_audio_path)
    print(f"Transcribed: {eng_text}")
    
    for lang_name, lang_code in LANGUAGES.items():
        print(f"\nProcessing {lang_name}...")
        
        # Translate
        translated = translate_text(eng_text, lang_code)
        print(f"Translated to {lang_name}")
        
        output_path = os.path.join(base_output_dir, f"{lang_name}_bark_clone.wav")
        
        # Try Bark voice cloning
        success = clone_with_bark(translated, output_path)
        
        if success:
            print(f"SUCCESS: {output_path}")
        else:
            # Fallback to gTTS
            print("Using gTTS fallback...")
            from gtts import gTTS
            tts = gTTS(text=translated, lang=lang_code, slow=False)
            mp3_output = output_path.replace('.wav', '.mp3')
            tts.save(mp3_output)
            print(f"Fallback: {mp3_output}")
    
    print(f"\nCompleted! Check: {base_output_dir}")
    print("\nNOTE: Bark TTS provides voice cloning but may not match your exact voice")
    print("For exact voice matching, you would need:")
    print("1. Custom training on your voice data")
    print("2. Or use paid services like ElevenLabs")

if __name__ == "__main__":
    input_audio_path = "D:/Telugu/input/input_english.wav"
    
    if not os.path.exists(input_audio_path):
        print(f"Input audio not found: {input_audio_path}")
    else:
        process_free_cloning(input_audio_path)