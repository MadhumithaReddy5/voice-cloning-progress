import whisper
from TTS.api import TTS
import os
from dotenv import load_dotenv
from googletrans import Translator

# 🛡️ Patch PyTorch unpickling (for XTTS config)
import torch
from torch.serialization import add_safe_globals
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsArgs, XttsAudioConfig
from TTS.config.shared_configs import BaseDatasetConfig
add_safe_globals([XttsConfig, XttsArgs, XttsAudioConfig, BaseDatasetConfig])

# 📦 Load environment variables
load_dotenv()

input_audio_path = os.getenv('INPUT_AUDIO_PATH')
output_audio_path = os.getenv('OUTPUT_AUDIO_PATH')
whisper_model_name = os.getenv('WHISPER_MODEL', 'base')
tts_model_name = os.getenv('TTS_MODEL', 'tts_models/multilingual/multi-dataset/xtts_v2')
tts_language = os.getenv('TTS_LANGUAGE', 'hi')
use_gpu = os.getenv('USE_GPU', 'False').lower() == 'true'

os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)

# 🎙️ Load Whisper model
print(f"🎙️ Loading Whisper model: {whisper_model_name}")
model = whisper.load_model(whisper_model_name)

# 🔍 Transcribe to English
print("🔍 Transcribing and translating audio to English...")
result = model.transcribe(input_audio_path, task='translate')
english_text = result['text']
print("📄 English Text:\n", english_text)

# 🌐 Translate English to formal Hindi using Google Translate
translator = Translator()
translation = translator.translate(english_text, src='en', dest='hi')
formal_hindi = translation.text
print("🗣️ Translated Formal Hindi:\n", formal_hindi)

# 💾 Save Hindi text to a file
hindi_text_path = os.path.join(os.path.dirname(output_audio_path), "translated_hindi_output.txt")
with open(hindi_text_path, "w", encoding="utf-8") as f:
    f.write(formal_hindi)

print(f"📝 Hindi text saved at: {hindi_text_path}")

# 🧬 Generate cloned Hindi audio
print("🧬 Generating cloned Hindi audio...")
tts = TTS(model_name=tts_model_name, progress_bar=True, gpu=use_gpu)
tts.tts_to_file(
    text=formal_hindi,
    speaker_wav=input_audio_path,
    language=tts_language,
    file_path=output_audio_path
)

print(f"✅ Output saved at: {output_audio_path}")
