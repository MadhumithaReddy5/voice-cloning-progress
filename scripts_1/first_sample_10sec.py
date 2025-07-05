import whisper
from TTS.api import TTS
import os
from googletrans import Translator
import torch
import librosa
import soundfile as sf

# 🛡️ Patch PyTorch unpickling (for XTTS config) - only if available
try:
    from torch.serialization import add_safe_globals
    from TTS.tts.configs.xtts_config import XttsConfig
    from TTS.tts.models.xtts import XttsArgs, XttsAudioConfig
    from TTS.config.shared_configs import BaseDatasetConfig
    add_safe_globals([XttsConfig, XttsArgs, XttsAudioConfig, BaseDatasetConfig])
except ImportError:
    # add_safe_globals not available in older PyTorch versions
    pass

# 📦 Direct file paths
input_audio_path = "D:\\Audio_Cloning_Project\\Input_audio\\Vivek_sir_20sec.wav"
output_audio_path = 'Results_audio_video/Vivek_sir_cloned_audio.wav'
text_output_path = 'Results_audio_video/Vivek_sir_translated_hindi_output.txt'
whisper_model_name = 'base'
tts_model_name = 'tts_models/multilingual/multi-dataset/xtts_v2'
tts_language = 'hi'
use_gpu = False

os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)

# 🎙️ Load Whisper model
print(f"🎙️ Loading Whisper model: {whisper_model_name}")
model = whisper.load_model(whisper_model_name)

# 🔍 Preprocess audio (alternative to FFmpeg)
def preprocess_audio(audio_path):
    try:
        # Load audio using librosa (doesn't require FFmpeg)
        audio, sr = librosa.load(audio_path, sr=16000)
        return audio
    except Exception as e:
        print(f"Error loading audio: {e}")
        return None

# 🔍 Transcribe to English
print("🔍 Transcribing and translating audio to English...")
try:
    result = model.transcribe(input_audio_path, task='translate')
except Exception as e:
    print(f"FFmpeg error detected. Using alternative audio loading...")
    audio_data = preprocess_audio(input_audio_path)
    if audio_data is not None:
        result = model.transcribe(audio_data, task='translate')
    else:
        raise e
english_text = result['text']
print("📄 English Text:\n", english_text)

# 🌐 Translate English to formal Hindi
translator = Translator()
translation = translator.translate(english_text, src='en', dest='hi')
formal_hindi = translation.text
print("🗣️ Translated Formal Hindi:\n", formal_hindi)

# 🤝 Convert to colloquial Hindi (80% Hindi + 20% English)
def make_colloquial_hinglish(text):
    replacements = {
        "ध्यान आकर्षित करने": "attention grab करने",
        "शानदार तरीका": "great तरीका",
        "कल्पना करें": "imagine करो",
        "शुरू करें": "start करो",
        "महत्वपूर्ण": "important",
        "पहले": "first",
        "शब्द": "word",
        "दर्शकों": "audience",
        "सेकंड": "seconds"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

colloquial_hinglish = make_colloquial_hinglish(formal_hindi)
print("✅ Colloquial Hindi (80-20 Hinglish):\n", colloquial_hinglish)

# 💾 Save text output
with open(text_output_path, "w", encoding="utf-8") as f:
    f.write(colloquial_hinglish)
print(f"📝 Hindi text saved at: {text_output_path}")

# 🧬 Generate cloned audio
print("🧬 Generating cloned Hindi audio...")
tts = TTS(model_name=tts_model_name, progress_bar=True, gpu=use_gpu)
tts.tts_to_file(
    text=colloquial_hinglish,
    speaker_wav=input_audio_path,
    language=tts_language,
    file_path=output_audio_path
)
print(f"✅ Output saved at: {output_audio_path}")
