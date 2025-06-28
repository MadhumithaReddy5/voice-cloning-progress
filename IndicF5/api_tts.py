from gtts import gTTS
import speech_recognition as sr
from googletrans import Translator
import os
import librosa
import soundfile as sf
import numpy as np

def english_audio_to_telugu_tts(input_audio_path, output_audio_path):
    """Convert English audio to Telugu TTS using Google APIs"""
    
    print("Processing English audio...")
    
    # Step 1: Speech Recognition
    recognizer = sr.Recognizer()
    
    # Load and convert audio for speech recognition
    audio_data, sr_rate = librosa.load(input_audio_path, sr=16000)
    
    # Convert to format for speech_recognition
    import io
    import wave
    audio_int16 = (audio_data * 32767).astype(np.int16)
    
    # Create in-memory wav file
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(16000)
        wav_file.writeframes(audio_int16.tobytes())
    
    wav_buffer.seek(0)
    
    try:
        # Recognize speech
        with sr.AudioFile(wav_buffer) as source:
            audio = recognizer.record(source)
        english_text = recognizer.recognize_google(audio)
        print(f"Recognized English text: {english_text}")
        
        # Step 2: Translate to Telugu
        translator = Translator()
        translated = translator.translate(english_text, src='en', dest='te')
        telugu_text = translated.text
        print(f"Translated Telugu text: {telugu_text}")
        
        # Step 3: Generate Telugu TTS
        tts = gTTS(text=telugu_text, lang='te', slow=False)
        tts.save(output_audio_path)
        
        print(f"Telugu TTS audio saved to: {output_audio_path}")
        return telugu_text
        
    except sr.UnknownValueError:
        print("Could not understand the audio")
        return None
    except sr.RequestError as e:
        print(f"Error with speech recognition: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def text_to_telugu_tts(text, output_path):
    """Convert text to Telugu TTS"""
    
    # Translate if English
    translator = Translator()
    try:
        detected = translator.detect(text)
        if detected.lang == 'en':
            translated = translator.translate(text, src='en', dest='te')
            telugu_text = translated.text
            print(f"Translated: {text} → {telugu_text}")
        else:
            telugu_text = text
    except:
        telugu_text = text
    
    # Generate TTS
    tts = gTTS(text=telugu_text, lang='te', slow=False)
    tts.save(output_path)
    print(f"Telugu TTS saved to: {output_path}")
    
    return telugu_text

def interactive_demo():
    """Interactive demo"""
    print("Telugu TTS using Google APIs")
    print("=" * 40)
    
    while True:
        print("\nChoose option:")
        print("1. Convert English audio to Telugu TTS")
        print("2. Convert text to Telugu TTS")
        print("3. Quit")
        
        choice = input("Enter choice (1/2/3): ").strip()
        
        if choice == '1':
            audio_path = input("Enter English audio file path: ").strip()
            if os.path.exists(audio_path):
                import time
                output_path = f"outputs/telugu_tts_{int(time.time())}.mp3"
                english_audio_to_telugu_tts(audio_path, output_path)
            else:
                print("File not found!")
                
        elif choice == '2':
            text = input("Enter English/Telugu text: ").strip()
            if text:
                import time
                output_path = f"outputs/text_tts_{int(time.time())}.mp3"
                text_to_telugu_tts(text, output_path)
                
        elif choice == '3':
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    interactive_demo()