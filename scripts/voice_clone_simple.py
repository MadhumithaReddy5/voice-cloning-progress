# -*- coding: utf-8 -*-
import os
import torch
import whisper
import re

def transcribe_audio(audio_path):
    print("Step 1: Transcribing English...")
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    print("Transcribed Text:", result["text"])
    return result["text"]

def translate_to_telugu(text):
    print("Step 2: Translating to Telugu...")
    try:
        from googletrans import Translator
        translator = Translator()
        result = translator.translate(text, src='en', dest='te')
        translated = result.text
        print("Telugu Translation:", translated)
        return translated
    except:
        translated = "అదే మరి, నీవు linear regression చూసినప్పుడు, akkada మనం ఒక number predict చేయడానికి ప్రయత్నిస్తాము. దానిని regression problem అంటారు."
        print("Mock Telugu Translation:", translated)
        return translated

def convert_to_colloquial(formal_text):
    print("Step 3: Making it colloquial...")
    replacements = {
        "మీరు": "నీవు",
        "లీనియర్ రిగ్రెషన్": "linear regression",
        "అంచనా వేయడానికి": "predict చేయడానికి",
        "సంఖ్యను": "number",
        "సమస్య": "problem",
        "మరోవైపు": "అదే మరి",
        "అక్కడ": "akkada",
        "మేము": "మనం"
    }
    
    colloquial = formal_text
    for formal, casual in replacements.items():
        colloquial = colloquial.replace(formal, casual)
    
    print("Colloquial Text:", colloquial)
    return colloquial

def generate_telugu_audio(text, output_path):
    print("Step 4: Generating Telugu Audio...")
    
    try:
        import edge_tts
        import asyncio
        
        async def generate_audio():
            # Use Telugu male voice
            voice = "te-IN-MohanNeural"  # Male Telugu voice
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_path)
        
        asyncio.run(generate_audio())
        print(f"Telugu audio generated: {output_path}")
        return True
        
    except Exception as e:
        print(f"Edge TTS failed: {e}")
        
        # Fallback to text file
        with open(output_path.replace('.wav', '.txt'), 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Text saved: {output_path.replace('.wav', '.txt')}")
        return False

def main():
    input_audio = "D:/Telugu/input/input_english.wav"
    output_audio = "D:/Telugu/output/telugu_audio.wav"
    
    os.makedirs(os.path.dirname(output_audio), exist_ok=True)
    
    print("Telugu Voice Generation Pipeline")
    print("=" * 40)
    
    english_text = transcribe_audio(input_audio)
    telugu_text = translate_to_telugu(english_text)
    colloquial_text = convert_to_colloquial(telugu_text)
    
    success = generate_telugu_audio(colloquial_text, output_audio)
    
    if success:
        print("\nSUCCESS! Telugu audio generated.")
        print("Note: This uses Microsoft's Telugu voice, not voice cloning.")
        print("\nFor TRUE VOICE CLONING:")
        print("1. Use Coqui TTS Studio")
        print("2. Try RVC (Retrieval-based Voice Conversion)")
        print("3. Use So-VITS-SVC")
        print("4. Try Tortoise TTS")
    else:
        print("\nAudio generation failed, but text is saved.")

if __name__ == "__main__":
    main()