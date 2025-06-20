import os
import torch
import shutil
import tempfile
import subprocess
from TTS.api import TTS
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
from transformers import pipeline
#from indictrans import Translator

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
    print("🔤 Transcribing English audio...")
    whisper_pipe = pipeline(
        model="openai/whisper-medium",
        task="transcribe",
        chunk_length_s=30,
        device=0 if device == "cuda" else -1
    )
    result = whisper_pipe(audio_path)
    return result["text"]

# Translate using IndicTrans2
import requests

def translate_text(text, target_lang):
    """
    Translate English text to target Indian language using IndicTrans2 server.
    Assumes server is running at http://localhost:5000/translate
    """
    try:
        payload = {
            "input": text,
            "src_lang": "en",
            "tgt_lang": target_lang
        }
        response = requests.post("http://localhost:5000/translate", json=payload)
        result = response.json()
        return result["output"]
    except Exception as e:
        print(f"❌ Translation failed: {e}")
        return text  # fallback to original


# Dummy colloquial converter (you can later customize this per language)
def make_colloquial(text, lang_code):
    # Example: informal tone tweak
    if lang_code == "hi":
        return text.replace("है", "है ना").replace("मैं", "मैं तो")
    elif lang_code == "te":
        return text.replace("వుంది", "ఉంది బాసూ")
    return text  # Default

# Voice cloning
def clone_voice(text, target_lang_code, ref_voice, output_path):
    print(f"🗣️ Cloning voice for {target_lang_code}...")
    try:
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        tts.tts_to_file(
            text=text,
            speaker_wav=ref_voice,
            language=target_lang_code,
            file_path=output_path
        )
        return True
    except Exception as e:
        print("❌ Voice cloning failed:", e)
        return False

# Main process
def process_audio_pipeline(input_audio_path):
    print("🚀 Starting pipeline...")

    base_output_dir = "D:/Telugu/output/final_outputs"
    os.makedirs(base_output_dir, exist_ok=True)

    # Step 1: Transcribe
    eng_text = transcribe_audio(input_audio_path)
    print(f"📄 Transcribed English: {eng_text}")

    # Step 2–4: For each Indian language
    for lang, code in LANGUAGES.items():
        print(f"\n🔁 Processing: {lang}")
        translated = translate_text(eng_text, code)
        colloquial = make_colloquial(translated, code)

        output_wav_path = os.path.join(base_output_dir, f"{lang}_cloned.wav")
        success = clone_voice(colloquial, code, input_audio_path, output_wav_path)

        if success:
            print(f"✅ {lang} voice cloned: {output_wav_path}")
        else:
            print(f"❌ Failed to generate {lang} audio")

    print("\n🎉 All done! Check your outputs in:", base_output_dir)

# ----------- RUN -------------
if __name__ == "__main__":
    input_audio_path = "D:/Telugu/input/input_english.wav"
    
    if not os.path.exists(input_audio_path):
        print(f"❌ Input audio not found: {input_audio_path}")
    else:
        process_audio_pipeline(input_audio_path)
