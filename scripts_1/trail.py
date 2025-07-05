import whisper
from TTS.api import TTS
import os
import time
from googletrans import Translator
from pydub import AudioSegment

# 🕒 Start timer
start_time = time.time()

# ✅ Manually set paths here (No .env required)
input_audio_path = r"D:\Audio_Cloning_Project\Results_audio_video\Vivek_sir_input.wav"
output_audio_path = r"D:\Audio_Cloning_Project\Results_audio_video\cloned_audio_final_123.wav"
text_output_path = r"D:\Audio_Cloning_Project\Results_audio_video\translated_colloquial_hindi_123.txt"

# ✅ Other settings
whisper_model_name = "base"
tts_model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
tts_language = "hi"
use_gpu = False

os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)

print(f"🔍 Transcribing and translating audio from: {input_audio_path}")

# 🎙️ Load Whisper model
print(f"🎙️ Loading Whisper model: {whisper_model_name}")
model = whisper.load_model(whisper_model_name)

# 🔍 Transcribe and translate to English
print("🔍 Transcribing and translating audio to English...")
result = model.transcribe(input_audio_path, task='translate')
english_text = result['text']
print("📄 English Text:\n", english_text)

# 🌐 Translate to formal Hindi
translator = Translator()
translation = translator.translate(english_text, src='en', dest='hi')
formal_hindi = translation.text
print("🗣️ Formal Hindi Translation:\n", formal_hindi)

# 🧠 Convert to colloquial Hindi (80-20 Hinglish)
def make_colloquial_hinglish(text):
    replacements = {
        "रैखिक प्रतिगमन": "linear regression",
        "संख्या": "number",
        "भविष्यवाणी": "prediction",
        "आउटपुट": "output",
        "समस्या": "problem",
        "मूल्यांकन": "evaluation",
        "मॉडल": "model",
        "डेटा": "data",
        "विश्लेषण": "analysis",
        "उदाहरण": "example"
    }
    for hindi, hinglish in replacements.items():
        text = text.replace(hindi, hinglish)
    return text

colloquial_hinglish = make_colloquial_hinglish(formal_hindi)
print("✅ Colloquial Hindi (80-20 Hinglish):\n", colloquial_hinglish)

# 💾 Save text output
with open(text_output_path, "w", encoding="utf-8") as f:
    f.write(colloquial_hinglish)
print(f"📝 Translated text saved at: {text_output_path}")

# 🔊 TTS initialization
print("🧬 Splitting text and generating audio in chunks...")
tts = TTS(model_name=tts_model_name, progress_bar=True, gpu=use_gpu)

# Split text into max 200 word chunks
def split_text_into_chunks(text, max_words=200):
    words = text.split()
    chunks = []
    current_chunk = []
    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_words:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

chunks = split_text_into_chunks(colloquial_hinglish, max_words=200)

# Generate and combine audio for all chunks
temp_chunk_paths = []
for i, chunk in enumerate(chunks):
    chunk_path = output_audio_path.replace(".wav", f"_chunk{i+1}.wav")
    print(f"🎧 Synthesizing chunk {i+1}/{len(chunks)}: {chunk}")
    tts.tts_to_file(
        text=chunk,
        speaker_wav=input_audio_path,
        language=tts_language,
        file_path=chunk_path
    )
    temp_chunk_paths.append(chunk_path)

# Combine audio chunks
combined = AudioSegment.empty()
for path in temp_chunk_paths:
    segment = AudioSegment.from_wav(path)
    combined += segment

combined.export(output_audio_path, format="wav")
print(f"✅ Final audio saved at: {output_audio_path}")

# Cleanup chunk files
for path in temp_chunk_paths:
    os.remove(path)

# ⏱️ Report execution time
end_time = time.time()
total_time = round(end_time - start_time, 2)
minutes = int(total_time // 60)
seconds = round(total_time % 60, 2)
print(f"⏱️ Total Execution Time: {minutes} minutes {seconds} seconds")
