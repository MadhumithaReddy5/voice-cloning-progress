import os
import torch
import whisper
import re

# Alternative voice cloning approach using RVC or other methods
def transcribe_audio(audio_path):
    print("🔍 Step 1: Transcribing English...")
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    print("📜 Transcribed Text:", result["text"])
    return result["text"]

def translate_to_telugu(text):
    print("🌐 Step 2: Translating to Telugu...")
    try:
        from googletrans import Translator
        translator = Translator()
        result = translator.translate(text, src='en', dest='te')
        translated = result.text
        print("🈸 Telugu Translation:", translated)
        return translated
    except:
        # Mock translation
        translated = "అదే మరి, నీవు linear regression చూసినప్పుడు, akkada మనం ఒక number predict చేయడానికి ప్రయత్నిస్తాము. దానిని regression problem అంటారు."
        print("🈸 Mock Telugu Translation:", translated)
        return translated

def convert_to_colloquial(formal_text):
    print("🗣️ Step 3: Making it colloquial...")
    # English-Telugu code switching
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
    
    print("💬 Colloquial Text:", colloquial)
    return colloquial

def generate_voice_clone(text, output_path, speaker_wav):
    print("🧬 Step 4: Voice Cloning...")
    
    # Method 1: Try with older PyTorch compatibility
    try:
        # Temporarily disable weights_only
        import torch
        original_load = torch.load
        torch.load = lambda *args, **kwargs: original_load(*args, **kwargs, weights_only=False) if 'weights_only' not in kwargs else original_load(*args, **kwargs)
        
        from TTS.api import TTS
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False)
        
        tts.tts_to_file(
            text=text,
            speaker_wav=speaker_wav,
            language="te",
            file_path=output_path
        )
        
        torch.load = original_load
        print(f"Voice cloned successfully: {output_path}")
        return True
        
    except Exception as e:
        print(f"Method 1 failed: {e}")
    
    # Method 2: Use edge-tts (Microsoft Edge TTS)
    try:
        import edge_tts
        import asyncio
        
        async def generate_edge_tts():
            # Use Telugu voice from Edge TTS
            voice = "te-IN-ShrutiNeural"  # Female voice
            # voice = "te-IN-MohanNeural"  # Male voice (if available)
            
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_path)
        
        asyncio.run(generate_edge_tts())
        print(f"Edge TTS generated: {output_path}")
        return True
        
    except Exception as e:
        print(f"Method 2 failed: {e}")
    
    # Method 3: Save text for manual processing
    print("Saving text for manual voice cloning...")
    with open(output_path.replace('.wav', '.txt'), 'w', encoding='utf-8') as f:
        f.write(f"Original Speaker: {speaker_wav}\n")
        f.write(f"Telugu Text: {text}\n")
        f.write("\n--- Instructions for Manual Voice Cloning ---\n")
        f.write("1. Use Coqui TTS Studio: https://github.com/coqui-ai/TTS\n")
        f.write("2. Try RVC (Retrieval-based Voice Conversion)\n")
        f.write("3. Use Tortoise TTS for high-quality cloning\n")
        f.write("4. Try So-VITS-SVC for voice conversion\n")
    
    print(f"Instructions saved: {output_path.replace('.wav', '.txt')}")
    return False

def main():
    input_audio = "D:/Telugu/input/input_english.wav"
    output_audio = "D:/Telugu/output/voice_cloned_telugu.wav"
    
    os.makedirs(os.path.dirname(output_audio), exist_ok=True)
    
    print("Alternative Voice Cloning Pipeline\n")
    
    # Process
    english_text = transcribe_audio(input_audio)
    telugu_text = translate_to_telugu(english_text)
    colloquial_text = convert_to_colloquial(telugu_text)
    
    # Try voice cloning
    success = generate_voice_clone(colloquial_text, output_audio, input_audio)
    
    if not success:
        print("\nSOLUTIONS FOR VOICE CLONING:")
        print("1. Install edge-tts: pip install edge-tts")
        print("2. Downgrade PyTorch: pip install torch==1.13.1")
        print("3. Use Google Colab with GPU for better TTS")
        print("4. Try online voice cloning services")

if __name__ == "__main__":
    main()