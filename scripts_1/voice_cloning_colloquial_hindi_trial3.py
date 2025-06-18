import whisper
from TTS.api import TTS
import os
import time
from dotenv import load_dotenv
from googletrans import Translator
from moviepy.editor import AudioFileClip

# 📦 Load environment variables
load_dotenv()

# 🎥 Input video to audio conversion
video_path = os.getenv('INPUT_VIDEO_PATH', 'Sample_video.mp4')
input_audio_path = 'temp_audio.wav'
output_audio_path = os.getenv('OUTPUT_AUDIO_PATH', 'Results_audio_video/cloned_audio_2.wav')
text_output_path = os.getenv('TEXT_OUTPUT_PATH', 'Results_audio_video/translated_hindi_output.txt')
whisper_model_name = os.getenv('WHISPER_MODEL', 'base')
tts_model_name = os.getenv('TTS_MODEL', 'tts_models/multilingual/multi-dataset/xtts_v2')
tts_language = os.getenv('TTS_LANGUAGE', 'hi')
use_gpu = os.getenv('USE_GPU', 'False').lower() == 'true'

os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)

start_time = time.time()

# 🎧 Extract audio from video
print(f"🎥 Extracting audio from {video_path}...")
audio_clip = AudioFileClip(video_path)
audio_clip.write_audiofile(input_audio_path, codec='pcm_s16le')

# 🎙️ Load Whisper model
print(f"\n🎙️ Loading Whisper model: {whisper_model_name}")
model = whisper.load_model(whisper_model_name)

# 🔍 Transcribe and translate
print("\n🔍 Transcribing and translating audio to English...")
result = model.transcribe(input_audio_path, task='translate')
english_text = result['text']
print("📄 English Text:\n", english_text)

# 🌐 Translate English to formal Hindi
translator = Translator()
translation = translator.translate(english_text, src='en', dest='hi')
formal_hindi = translation.text
print("\n🗣️ Translated Formal Hindi:\n", formal_hindi)

# 🤝 Convert to colloquial Hindi (80% Hindi + 20% English)
def make_colloquial_hinglish(text):
    replacements = {
        "प्रतिगमन": "regression",
        "डेटा सेट": "dataset",
        "मॉडल": "model",
        "पूर्वानुमान": "prediction",
        "विश्लेषण": "analysis",
        "रूप में": "as",
        "प्रशिक्षण": "training",
        "परिणाम": "result",
        "तथ्य": "fact",
        "विशेषता": "feature",
        "महत्वपूर्ण": "important",
        "प्रदर्शन": "performance",
        "त्रुटि": "error"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

colloquial_hinglish = make_colloquial_hinglish(formal_hindi)
print("\n✅ Colloquial Hindi (80-20 Hinglish):\n", colloquial_hinglish)

# 💾 Save text output
with open(text_output_path, "w", encoding="utf-8") as f:
    f.write(colloquial_hinglish)
print(f"\n📝 Hindi text saved at: {text_output_path}")

# 🧬 Generate cloned audio
print("\n🧬 Generating cloned Hindi audio...")
tts = TTS(model_name=tts_model_name, progress_bar=True, gpu=use_gpu)
tts.tts_to_file(
    text=colloquial_hinglish,
    speaker_wav=input_audio_path,
    language=tts_language,
    file_path=output_audio_path
)
print(f"\n✅ Output saved at: {output_audio_path}")

end_time = time.time()
print(f"\n⏱️ Total processing time: {round(end_time - start_time, 2)} seconds")
