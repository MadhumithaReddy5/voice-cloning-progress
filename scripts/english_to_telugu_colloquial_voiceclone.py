import os
import torch
import whisper
import re
from TTS.api import TTS

# Set device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Step 1: Transcribe English audio using Whisper
def transcribe_audio(audio_path):
    print("🔍 Step 1: Transcribing English...")
    model = whisper.load_model("base", device=device)
    result = model.transcribe(audio_path)
    print("📜 Transcribed Text: ", result["text"])
    return result["text"]

# Step 2: Translate English to Telugu
def translate_to_telugu(text):
    print("🌐 Step 2: Translating to Telugu...")
    print("📥 Input to translation:", text)
    
    try:
        # Try using Google Translate as a simpler alternative
        from googletrans import Translator
        translator = Translator()
        result = translator.translate(text, src='en', dest='te')
        translated = result.text
        print("🈸 Formal Telugu Translation:", translated)
        return translated
    except ImportError:
        # Fallback to a simple mock translation for testing
        print("⚠️ Google Translate not available, using mock translation")
        translated = "మరుక వైపు, మీరు లీనియర్ రిగ్రెషన్ చూడాలి, అక్కడ మనం ఒక సంఖ్యను అనుమానించడానికి ప్రయత్నిస్తాము. అది రిగ్రెషన్ సమస్య అని అన్నారు."
        print("🈸 Mock Telugu Translation:", translated)
        return translated

# Step 3: Convert to Colloquial Telugu with English code-switching
def convert_to_colloquial_telugu(formal_text):
    print("🗣️ Step 3: Converting to Colloquial Telugu with English mixing...")
    
    # Telugu formality replacements
    replacements = {
        "మీరు": "నీవు",
        "చేయండి": "చేయ్",
        "వద్దు": "వెయ్",
        "అవును": "అబ్బో",
        "లేదు": "లేదురా",
        "వివరణ": "మాటలు",
        "మేము": "మనం",
        "అంచనా వేయడానికి": "predict చేయడానికి",
        "సమస్య": "problem"
    }
    
    # English-Telugu code-switching for technical terms
    tech_replacements = {
        "లీనియర్ రిగ్రెషన్": "linear regression",
        "రిగ్రెషన్ సమస్య": "regression problem",
        "సంఖ్యను": "number"
    }
    
    colloquial = formal_text
    
    # Apply Telugu formality changes
    for formal, casual in replacements.items():
        colloquial = re.sub(formal, casual, colloquial)
    
    # Apply English code-switching for technical terms
    for telugu_term, english_term in tech_replacements.items():
        colloquial = re.sub(telugu_term, english_term, colloquial)
    
    # Add colloquial connectors and fillers
    colloquial = re.sub(r'మరోవైపు,', 'అదే మరి,', colloquial)  # "On the other hand" -> "And then"
    colloquial = re.sub(r'అక్కడ', 'akkada', colloquial)  # Keep "there" in English
    
    print("💬 Colloquial Telugu Text: ", colloquial)
    return colloquial

# Step 4: Voice cloning with proper male voice preservation
def generate_telugu_voice(text, output_path, speaker_wav=None):
    print("🧬 Step 4: Cloning Voice to Telugu Speech...")
    
    try:
        # Fix PyTorch safe globals issue
        import torch
        torch.serialization.add_safe_globals([
            'TTS.tts.configs.xtts_config.XttsConfig',
            'TTS.vocoder.configs.hifigan_config.HifiganConfig',
            'TTS.tts.layers.xtts.tokenizer.VoiceBpeTokenizer',
            'TTS.tts.models.xtts.XTTS'
        ])
        
        # Use XTTS v2 model for voice cloning
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False, gpu=torch.cuda.is_available())
        
        if speaker_wav and os.path.exists(speaker_wav):
            print(f"🎤 Cloning male voice from: {speaker_wav}")
            
            # Generate Telugu audio with voice cloning
            tts.tts_to_file(
                text=text,
                speaker_wav=speaker_wav,
                language="te",
                file_path=output_path
            )
            print(f"🔊 Male voice cloned Telugu audio saved at: {output_path}")
        else:
            print("⚠️ No speaker reference found")
            return
        
    except Exception as e:
        print(f"⚠️ XTTS Error: {str(e)}")
        print("🔧 Trying with weights_only=False...")
        
        try:
            # Set torch.load to use weights_only=False
            original_load = torch.load
            torch.load = lambda *args, **kwargs: original_load(*args, **kwargs, weights_only=False)
            
            # Try again with modified torch.load
            tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False, gpu=torch.cuda.is_available())
            
            tts.tts_to_file(
                text=text,
                speaker_wav=speaker_wav,
                language="te",
                file_path=output_path
            )
            
            # Restore original torch.load
            torch.load = original_load
            
            print(f"🔊 Voice cloning successful: {output_path}")
            
        except Exception as e2:
            print(f"⚠️ All voice cloning methods failed: {str(e2)}")
            print("📝 Saving text to file instead...")
            with open(output_path.replace('.wav', '.txt'), 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"📝 Telugu text saved at: {output_path.replace('.wav', '.txt')}")
            print("\n💡 Voice cloning IS possible! Try these solutions:")
            print("1. Downgrade PyTorch: pip install torch==1.13.1")
            print("2. Use Coqui TTS Studio for better voice cloning")
            print("3. Try RVC (Retrieval-based Voice Conversion) for voice cloning")
            print("4. Use Tortoise TTS for high-quality voice cloning")

# Full pipeline
def main(input_audio_path, output_audio_path):
    english_text = transcribe_audio(input_audio_path)
    telugu_formal = translate_to_telugu(english_text)
    telugu_colloquial = convert_to_colloquial_telugu(telugu_formal)
    generate_telugu_voice(telugu_colloquial, output_audio_path, speaker_wav=input_audio_path)

# Example run
if __name__ == "__main__":
    input_audio = "D:/Telugu/input/input_english.wav"
    output_audio = "D:/Telugu/output/output_colloquial_telugu.wav"
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_audio), exist_ok=True)
    
    print(f"🎤 Input audio: {input_audio}")
    print(f"🔊 Output audio: {output_audio}")
    print("🎆 Starting English to Colloquial Telugu Voice Cloning Pipeline...\n")
    main(input_audio, output_audio)