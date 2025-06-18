import os
import time
import torch
import whisper
import re
from TTS.api import TTS
from transformers import AutoTokenizer
from deep_translator import GoogleTranslator
from pydub import AudioSegment

start_time = time.time()

# 🎙️ Load Whisper model
print("🎙️ Loading Whisper...")
model = whisper.load_model("base")

# 🎧 Input audio path
input_audio_path = "D:\\Audio_Cloning_Project\\Input_audio\\audio 5min vivek sir.wav"

# 📝 Transcribe English text
result = model.transcribe(input_audio_path)
english_text = result["text"]
print("📄 English Text:\n", english_text)

# 🌐 Translate to formal Hindi
formal_hindi = GoogleTranslator(source="en", target="hi").translate(english_text)
print("🗣️ Formal Hindi:\n", formal_hindi)

# ✅ Improved Hinglish mixing logic (targeting 70% Hindi, 30% English)
def convert_to_colloquial_hinglish(text):
    keyword_map = {
        "टोकन": "token", "टोकनाइज़ेशन": "tokenization", "एम्बेडिंग": "embedding", "वेक्टर": "vector",
        "मॉडल": "model", "भाषा मॉडल": "language model", "इनपुट": "input", "आउटपुट": "output",
        "टेक्स्ट": "text", "वाक्य": "sentence", "एनएलपी": "NLP", "प्रोसेसिंग": "processing",
        "क्लासिफायर": "classifier", "ट्रेनिंग": "training", "डेटासेट": "dataset", "अटेंशन": "attention",
        "लेयर": "layer", "सिक्वेंस": "sequence", "फीचर": "feature", "लेबल": "label",
        "सटीकता": "accuracy", "हानि": "loss", "भविष्यवाणी": "prediction", "संदर्भ": "context",
        "डिकोडर": "decoder", "एनकोडर": "encoder", "न्यूरल नेटवर्क": "neural network",
        "पैरामीटर": "parameter", "रिप्रेजेंटेशन": "representation", "पाइपलाइन": "pipeline",
        "सिंटैक्स": "syntax", "सैमान्टिक्स": "semantics", "कोड": "code", "डेटा": "data",
        "सूची": "list", "वैरिएबल": "variable", "क्लास": "class", "फ़ंक्शन": "function"
    }

    for hindi_word, eng_word in keyword_map.items():
        text = re.sub(rf"\b{re.escape(hindi_word)}\b", eng_word, text)
    return text

colloquial_text = convert_to_colloquial_hinglish(formal_hindi)
print("✅ Colloquial Hindi (Explicit 70:30 Hinglish):\n", colloquial_text)

# 🧠 Load tokenizer and TTS
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-hin")

# 🪓 Split text into safe chunks
def split_text_by_tokens(text, max_tokens=380):
    text = re.sub(r'([।.!?])(?=\S)', r'\1 ', text)
    sentences = re.split(r'(?<=[।.!?])\s+', text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if not sentence.strip():
            continue
        token_count = tokenizer(sentence, return_tensors="pt").input_ids.shape[1]
        current_token_count = tokenizer(current_chunk, return_tensors="pt").input_ids.shape[1] if current_chunk else 0

        if current_token_count + token_count < max_tokens:
            current_chunk = (current_chunk + " " + sentence).strip()
        else:
            if current_chunk:
                chunks.append(current_chunk)
            if token_count >= max_tokens:
                words = sentence.split()
                sub_chunk = ""
                for word in words:
                    test = f"{sub_chunk} {word}".strip()
                    if tokenizer(test, return_tensors="pt").input_ids.shape[1] < max_tokens:
                        sub_chunk = test
                    else:
                        chunks.append(sub_chunk)
                        sub_chunk = word
                if sub_chunk:
                    chunks.append(sub_chunk)
                current_chunk = ""
            else:
                current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

chunks = split_text_by_tokens(colloquial_text)
print(f"🧩 Text split into {len(chunks)} chunks")

# 🔊 Synthesize and concatenate all audio chunks
speaker_wav = input_audio_path
language = "hi"
final_audio = AudioSegment.empty()

for idx, chunk in enumerate(chunks):
    print(f"🎧 Synthesizing chunk {idx+1}/{len(chunks)}:\n{chunk[:60]}...")
    temp_path = f"temp_output_{idx+1}.wav"
    tts.tts_to_file(text=chunk, speaker_wav=speaker_wav, language=language, file_path=temp_path)
    final_audio += AudioSegment.from_wav(temp_path)
    os.remove(temp_path)

# 💾 Save final voice cloned audio
final_output_path = "final_5_min_audio_colloquial.wav"
final_audio.export(final_output_path, format="wav")
print("✅ Final voice cloned audio saved to:", final_output_path)

# ⏱️ Execution time
end_time = time.time()
print(f"⏱️ Total Execution Time: {round((end_time - start_time) / 60, 2)} minutes")
