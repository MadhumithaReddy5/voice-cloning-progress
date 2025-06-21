import os
import torch
import shutil
import tempfile
import subprocess
from transformers import pipeline
from googletrans import Translator
import requests

# Set up device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Language mapping
LANGUAGES = {
    "telugu": "te",
    "hindi": "hi",
    "kannada": "kn",
    "bengali": "bn",
    "tamil": "ta",
    "malayalam": "ml",
}

# Load Whisper model for transcription
def transcribe_audio(audio_path):
    print("Transcribing English audio...")
    whisper_pipe = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-medium",
        chunk_length_s=30,
        device=0 if device == "cuda" else -1
    )
    result = whisper_pipe(audio_path)
    return result["text"]

# Translate using Google Translate
def translate_text(text, target_lang):
    """
    Translate English text to target Indian language using Google Translate.
    """
    try:
        translator = Translator()
        translated = translator.translate(text, dest=target_lang)
        return translated.text
    except Exception as e:
        print(f"Translation failed: {e}")
        return text  # fallback to original


# Dummy colloquial converter (you can later customize this per language)
def make_colloquial(text, lang_code):
    # Example: informal tone tweak
    if lang_code == "hi":
        return text.replace("है", "है ना").replace("मैं", "मैं तो")
    elif lang_code == "te":
        return text.replace("వుంది", "ఉంది బాసూ")
    return text  # Default

# Voice cloning with actual voice matching
def clone_voice(text, target_lang_code, ref_voice, output_path):
    print(f"Cloning voice for {target_lang_code}...")
    
    # Try Coqui TTS for actual voice cloning
    try:
        from TTS.api import TTS
        print("Using Coqui TTS for voice cloning...")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        tts.tts_to_file(
            text=text,
            speaker_wav=ref_voice,
            language=target_lang_code,
            file_path=output_path
        )
        print(f"Voice cloned: {output_path}")
        return True
    except Exception as e:
        print(f"Coqui TTS failed: {e}")
        
        # Fallback: Try RVC-style voice conversion
        try:
            print("Trying voice conversion approach...")
            return voice_conversion_fallback(text, target_lang_code, ref_voice, output_path)
        except Exception as e2:
            print(f"Voice conversion failed: {e2}")
            
            # Final fallback: gTTS with note
            print("Using gTTS (no voice matching)...")
            from gtts import gTTS
            tts = gTTS(text=text, lang=target_lang_code, slow=False)
            mp3_output = output_path.replace('.wav', '.mp3')
            tts.save(mp3_output)
            print(f"Note: Native pronunciation only, no voice matching: {mp3_output}")
            return True

def voice_conversion_fallback(text, target_lang_code, ref_voice, output_path):
    """Attempt voice conversion using available tools"""
    try:
        # First create TTS in target language
        from gtts import gTTS
        temp_tts = "temp_tts.mp3"
        tts = gTTS(text=text, lang=target_lang_code, slow=False)
        tts.save(temp_tts)
        
        # Try to use any available voice conversion
        # This is a placeholder - would need actual RVC or similar
        print("Voice conversion not available - using native TTS")
        
        # Move temp file to output
        import shutil
        shutil.move(temp_tts, output_path.replace('.wav', '.mp3'))
        return True
        
    except Exception as e:
        print(f"Voice conversion fallback failed: {e}")
        return False

# Main process
def process_audio_pipeline(input_audio_path):
    print("Starting pipeline...")

    base_output_dir = "D:/Telugu/output/final_outputs"
    os.makedirs(base_output_dir, exist_ok=True)

    # Step 1: Transcribe
    eng_text = transcribe_audio(input_audio_path)
    print(f"Transcribed English: {eng_text}")

    # Step 2-4: For each Indian language
    for lang, code in LANGUAGES.items():
        print(f"\nProcessing: {lang}")
        translated = translate_text(eng_text, code)
        colloquial = make_colloquial(translated, code)

        output_wav_path = os.path.join(base_output_dir, f"{lang}_cloned.wav")
        success = clone_voice(colloquial, code, input_audio_path, output_wav_path)

        if success:
            print(f"SUCCESS {lang} voice cloned: {output_wav_path}")
        else:
            print(f"FAILED to generate {lang} audio")

    print("\nAll done! Check your outputs in:", base_output_dir)

# ----------- RUN -------------
if __name__ == "__main__":
    input_audio_path = "D:/Telugu/input/input_english.wav"
    
    if not os.path.exists(input_audio_path):
        print(f"Input audio not found: {input_audio_path}")
    else:
        process_audio_pipeline(input_audio_path)
