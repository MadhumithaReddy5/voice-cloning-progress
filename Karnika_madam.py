import os
import torch
import whisper
import re
from TTS.api import TTS
from transformers import AutoTokenizer
from deep_translator import GoogleTranslator
from pydub import AudioSegment
from pydub.playback import play
import tempfile

# Load Whisper
print("🎙️ Loading Whisper...")
model = whisper.load_model("base")

# Input audio path
input_audio_path = r"D:\Hindi Output\Input audio\speaker2.wav"

#input_audio_path = "D:\Hindi Output\Input audio\speaker2.wav"

# Transcribe
result = model.transcribe(input_audio_path)
english_text = result["text"]
print("📄 English Text:\n ", english_text)

# Translate to Formal Hindi
formal_hindi = GoogleTranslator(source="en", target="hi").translate(english_text)
print("🗣️ Formal Hindi:\n", formal_hindi)

# Convert to Colloquial Hindi (80% Hindi + 20% English)
def convert_to_colloquial_hinglish(text):
    replacements = {
        "व्यक्ति": "बंदा",
        "उपकरण": "device",
        "निर्णय": "decision",
        "विचारों": "thoughts",
        "पाठ्यक्रम": "process",
        "नियंत्रित": "controlled",
        "उदाहरण": "example",
        "संचालित होता है": "operate होता है",
        "स्वायत्त रोबोट": "autonomous robot",
        "देख सकते हैं": "देख सकते हो",
        "जैसा कि": "जैसे कि",
        "जो आदमी": "जो बंदा"
    }

    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


colloquial_text = convert_to_colloquial_hinglish(formal_hindi)
print("✅ Colloquial Hindi (80-20 Hinglish):\n", colloquial_text)

# Load tokenizer and TTS
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-hin")

# ✅ Split text safely
def split_text_by_tokens(text, max_tokens=380):
    # Add space after punctuation if missing
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
                # Break long sentence
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

# 🔀 Split the text
chunks = split_text_by_tokens(colloquial_text)
print(f"🧩 Text split into {len(chunks)} chunks")

# Load speaker voice sample
speaker_wav = input_audio_path
language = "hi"
output_paths = []

# 🔊 Synthesize each chunk
for idx, chunk in enumerate(chunks):
    print(f"🎧 Synthesizing chunk {idx + 1}/{len(chunks)}:\n{chunk[:60]}...")
    out_path = f"output_chunk_{idx + 1}.wav"
    tts.tts_to_file(
        text=chunk,
        speaker_wav=speaker_wav,
        language=language,
        file_path=out_path
    )
    output_paths.append(out_path)

# 🔗 Concatenate chunks into one audio
combined = AudioSegment.empty()
for path in output_paths:
    segment = AudioSegment.from_wav(path)
    combined += segment

# 🔐 Save final output
final_output = "final_cloned_output.wav"
combined.export(final_output, format="wav")
print("✅ Final voice cloned audio saved to:", final_output)

# ✅ Optional: Play it
# play(AudioSegment.from_wav(final_output))
