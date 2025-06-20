"""
COQUI TTS EXTENT TEST
====================
Let's test how far Coqui can work with Telugu and voice cloning
"""

import os
import sys

def test_coqui_basic():
    """Test basic Coqui TTS functionality"""
    print("=" * 50)
    print("TEST 1: Basic Coqui TTS")
    print("=" * 50)
    
    try:
        from TTS.api import TTS
        print("✓ Coqui TTS imported successfully")
        
        # List available models
        print("\nAvailable TTS models:")
        tts = TTS()
        models = tts.list_models()
        
        # Show multilingual models
        multilingual_models = [m for m in models if 'multilingual' in m.lower()]
        print("Multilingual models:")
        for model in multilingual_models[:5]:  # Show first 5
            print(f"  - {model}")
            
        return True
        
    except Exception as e:
        print(f"✗ Coqui TTS failed: {e}")
        return False

def test_coqui_xtts():
    """Test XTTS model specifically"""
    print("\n" + "=" * 50)
    print("TEST 2: XTTS Voice Cloning Model")
    print("=" * 50)
    
    try:
        import torch
        
        # Fix PyTorch loading issues
        torch.serialization.add_safe_globals([
            'TTS.tts.configs.xtts_config.XttsConfig',
            'TTS.vocoder.configs.hifigan_config.HifiganConfig',
            'TTS.tts.layers.xtts.tokenizer.VoiceBpeTokenizer',
            'TTS.tts.models.xtts.XTTS'
        ])
        
        from TTS.api import TTS
        
        print("Loading XTTS model...")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False)
        print("✓ XTTS model loaded successfully")
        
        return tts
        
    except Exception as e:
        print(f"✗ XTTS loading failed: {e}")
        return None

def test_telugu_phonetic(tts):
    """Test Telugu with phonetic spelling"""
    print("\n" + "=" * 50)
    print("TEST 3: Telugu Phonetic Approach")
    print("=" * 50)
    
    if not tts:
        print("✗ No TTS model available")
        return False
    
    try:
        # Telugu in phonetic English
        telugu_phonetic = "Ade mari, neevu linear regression choosinappudu, akkada manam oka number predict cheyadaniki prayatnistamu. Danini regression problem antaru."
        
        print("Generating Telugu (phonetic)...")
        output_path = "D:/Telugu/output/coqui_telugu_phonetic.wav"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        tts.tts_to_file(
            text=telugu_phonetic,
            language="en",
            file_path=output_path
        )
        
        print(f"✓ Telugu phonetic audio created: {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ Telugu phonetic failed: {e}")
        return False

def test_voice_cloning(tts):
    """Test voice cloning with your audio"""
    print("\n" + "=" * 50)
    print("TEST 4: Voice Cloning")
    print("=" * 50)
    
    if not tts:
        print("✗ No TTS model available")
        return False
    
    speaker_wav = "D:/Telugu/input/input_english.wav"
    
    if not os.path.exists(speaker_wav):
        print(f"✗ Speaker audio not found: {speaker_wav}")
        return False
    
    try:
        # Test 1: English with your voice
        print("Test 4a: English with your voice...")
        english_text = "Hello, this is a test of voice cloning with Coqui TTS."
        
        tts.tts_to_file(
            text=english_text,
            speaker_wav=speaker_wav,
            language="en",
            file_path="D:/Telugu/output/coqui_english_cloned.wav"
        )
        print("✓ English voice cloning successful")
        
        # Test 2: Telugu phonetic with your voice
        print("Test 4b: Telugu phonetic with your voice...")
        telugu_phonetic = "Ade mari, neevu linear regression choosinappudu."
        
        tts.tts_to_file(
            text=telugu_phonetic,
            speaker_wav=speaker_wav,
            language="en",
            file_path="D:/Telugu/output/coqui_telugu_voice_cloned.wav"
        )
        print("✓ Telugu phonetic voice cloning successful")
        
        return True
        
    except Exception as e:
        print(f"✗ Voice cloning failed: {e}")
        return False

def test_hindi_approach(tts):
    """Test using Hindi for better Telugu phonetics"""
    print("\n" + "=" * 50)
    print("TEST 5: Hindi Approach (Similar Phonetics)")
    print("=" * 50)
    
    if not tts:
        print("✗ No TTS model available")
        return False
    
    try:
        # Hindi text (closer to Telugu phonetically)
        hindi_text = "दूसरी ओर, जब आपने linear regression देखा है, वहाँ हम एक number predict करने की कोशिश करते हैं।"
        
        speaker_wav = "D:/Telugu/input/input_english.wav"
        
        if os.path.exists(speaker_wav):
            print("Generating Hindi with voice cloning...")
            tts.tts_to_file(
                text=hindi_text,
                speaker_wav=speaker_wav,
                language="hi",
                file_path="D:/Telugu/output/coqui_hindi_cloned.wav"
            )
            print("✓ Hindi voice cloning successful")
        else:
            print("Generating Hindi without voice cloning...")
            tts.tts_to_file(
                text=hindi_text,
                language="hi",
                file_path="D:/Telugu/output/coqui_hindi_basic.wav"
            )
            print("✓ Hindi basic generation successful")
        
        return True
        
    except Exception as e:
        print(f"✗ Hindi approach failed: {e}")
        return False

def test_direct_telugu(tts):
    """Test direct Telugu script"""
    print("\n" + "=" * 50)
    print("TEST 6: Direct Telugu Script")
    print("=" * 50)
    
    if not tts:
        print("✗ No TTS model available")
        return False
    
    try:
        # Direct Telugu script
        telugu_script = "అదే మరి, నీవు లినియర్ రిగ్రెషన్ చూసినప్పుడు, అక్కడ మనం ఒక నంబర్ ప్రిడిక్ట్ చేయడానికి ప్రయత్నిస్తాము."
        
        print("Attempting direct Telugu script...")
        tts.tts_to_file(
            text=telugu_script,
            language="te",  # Telugu language code
            file_path="D:/Telugu/output/coqui_direct_telugu.wav"
        )
        print("✓ Direct Telugu successful!")
        return True
        
    except Exception as e:
        print(f"✗ Direct Telugu failed: {e}")
        
        # Try with English language model
        try:
            print("Trying Telugu script with English model...")
            tts.tts_to_file(
                text=telugu_script,
                language="en",
                file_path="D:/Telugu/output/coqui_telugu_via_english.wav"
            )
            print("✓ Telugu via English model successful!")
            return True
        except Exception as e2:
            print(f"✗ Telugu via English also failed: {e2}")
            return False

def main():
    print("COQUI TTS EXTENT TEST")
    print("Testing how far we can push Coqui with Telugu and voice cloning")
    print("=" * 60)
    
    # Test 1: Basic functionality
    if not test_coqui_basic():
        print("\n❌ RESULT: Coqui TTS not working at all")
        print("Fix: pip install numpy==1.24.3 torch==1.13.1")
        return
    
    # Test 2: Load XTTS
    tts = test_coqui_xtts()
    
    if not tts:
        print("\n❌ RESULT: XTTS model not loading")
        print("This is the main issue - PyTorch compatibility")
        return
    
    # Test 3-6: Various approaches
    results = {
        "Telugu Phonetic": test_telugu_phonetic(tts),
        "Voice Cloning": test_voice_cloning(tts),
        "Hindi Approach": test_hindi_approach(tts),
        "Direct Telugu": test_direct_telugu(tts)
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    
    working_methods = []
    for method, success in results.items():
        status = "✓ WORKS" if success else "✗ FAILED"
        print(f"{method}: {status}")
        if success:
            working_methods.append(method)
    
    if working_methods:
        print(f"\n🎉 SUCCESS: {len(working_methods)} methods working!")
        print("Working methods:", ", ".join(working_methods))
        print("\nCheck D:/Telugu/output/ for generated audio files")
    else:
        print("\n❌ NO METHODS WORKING")
        print("Recommendation: Use ElevenLabs or Google Colab RVC")

if __name__ == "__main__":
    main()