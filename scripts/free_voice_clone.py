#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FREE Voice Cloning Solution
Uses Tortoise TTS (free alternative to Coqui)
"""

import os
import torch
from transformers import pipeline
from googletrans import Translator

# Set up device
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

def clone_voice_tortoise(text, target_lang_code, ref_voice, output_path):
    """Try Tortoise TTS for voice cloning"""
    try:
        import tortoise.api
        print("Using Tortoise TTS...")
        
        tts = tortoise.api.TextToSpeech()
        audio = tts.tts_with_preset(
            text, 
            voice_samples=[ref_voice],
            preset='fast'
        )
        
        import torchaudio
        torchaudio.save(output_path, audio.squeeze(0).cpu(), 24000)
        return True
        
    except ImportError:
        print("Tortoise TTS not available")
        return False
    except Exception as e:
        print(f"Tortoise failed: {e}")
        return False

def clone_voice_bark(text, output_path):
    """Try Bark TTS for voice cloning"""
    try:
        from bark import SAMPLE_RATE, generate_audio, preload_models
        from scipy.io.wavfile import write as write_wav
        
        print("Using Bark TTS...")
        preload_models()
        
        audio_array = generate_audio(text)
        write_wav(output_path, SAMPLE_RATE, audio_array)
        return True
        
    except ImportError:
        print("Bark TTS not available")
        return False
    except Exception as e:
        print(f"Bark failed: {e}")
        return False

def process_free_voice_cloning(input_audio_path):
    print("FREE Voice Cloning Pipeline")
    print("=" * 40)
    
    base_output_dir = "D:/Telugu/output/free_voice_clone"
    os.makedirs(base_output_dir, exist_ok=True)
    
    # Transcribe
    eng_text = transcribe_audio(input_audio_path)
    print(f"Transcribed: {eng_text}")
    
    for lang_name, lang_code in LANGUAGES.items():
        print(f"\nProcessing {lang_name}...")
        
        # Translate
        translated = translate_text(eng_text, lang_code)
        print(f"Translated to {lang_name}")
        
        output_path = os.path.join(base_output_dir, f"{lang_name}_free_clone.wav")
        
        # Try different free voice cloning methods
        success = False
        
        # Method 1: Tortoise TTS
        if not success:
            success = clone_voice_tortoise(translated, lang_code, input_audio_path, output_path)
        
        # Method 2: Bark TTS
        if not success:
            success = clone_voice_bark(translated, output_path)
        
        # Method 3: Fallback to gTTS
        if not success:
            print("Using gTTS fallback...")
            from gtts import gTTS
            tts = gTTS(text=translated, lang=lang_code, slow=False)
            mp3_output = output_path.replace('.wav', '.mp3')
            tts.save(mp3_output)
            print(f"Fallback saved: {mp3_output}")
        else:
            print(f"SUCCESS: {output_path}")
    
    print(f"\nCompleted! Check: {base_output_dir}")

if __name__ == "__main__":
    input_audio_path = "D:/Telugu/input/input_english.wav"
    
    if not os.path.exists(input_audio_path):
        print(f"Input audio not found: {input_audio_path}")
    else:
        process_free_voice_cloning(input_audio_path)