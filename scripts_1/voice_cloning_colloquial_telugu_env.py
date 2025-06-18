import whisper
from TTS.api import TTS
import os
from dotenv import load_dotenv

# ✅ Patch for PyTorch 2.6+ to allow XTTS globals
import torch
from torch.serialization import add_safe_globals
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsArgs, XttsAudioConfig
from TTS.config.shared_configs import BaseDatasetConfig

add_safe_globals([XttsConfig, XttsArgs, XttsAudioConfig, BaseDatasetConfig])

# 📄 Load environment variables
load_dotenv()

# 🎯 Read values from .env
input_audio_path = os.getenv('INPUT_AUDIO_PATH')
output_audio_path = os.getenv('OUTPUT_AUDIO_PATH')
whisper_model_name = os.getenv('WHISPER_MODEL', 'base')
tts_model_name = os.getenv('TTS_MODEL', 'tts_models/multilingual/multi-dataset/xtts_v2')
tts_language = os.getenv('TTS_LANGUAGE', 'te')  # Use ISO 639-1 code for Telugu
use_gpu = os.getenv('USE_GPU', 'False').lower() == 'true'

# 🗂️ Ensure output path exists
os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)

# 🔊 Load Whisper
print(f"🎙️ Loading Whisper model: {whisper_model_name}")
model = whisper.load_model(whisper_model_name)

# 🎧 Transcribe
print("🔍 Transcribing and translating audio to English...")
result = model.transcribe(input_audio_path, task='translate')
english_text = result['text']
print("📄 English Text:\n", english_text)

# 💬 Colloquial Telugu conversion
def make_colloquial(text):
    replacements = {
        "hello": "హాయ్",
        "how are you": "ఎలా ఉన్నావు",
        "attention": "మనసు పెట్టు",
        "imagine": "ఊహించు",
        "super important": "చాలా ముఖ్యం",
        "audience": "ప్రేక్షకులు",
        "grip": "పట్టుకో",
        "start": "మొదలు పెట్టు"
    }
    for k, v in replacements.items():
        text = text.lower().replace(k, v)
    return text

print("🗣️ Converting to colloquial Telugu...")
colloquial_telugu = make_colloquial(english_text)
print("✅ Telugu (colloquial):\n", colloquial_telugu)

# 🔈 Voice cloning
print("🧬 Generating cloned Telugu audio...")
tts = TTS(model_name=tts_model_name, progress_bar=True, gpu=use_gpu)
tts.tts_to_file(
    text=colloquial_telugu,
    speaker_wav=input_audio_path,
    language=tts_language,
    file_path=output_audio_path
)

print(f"✅ Output saved at: {output_audio_path}")
