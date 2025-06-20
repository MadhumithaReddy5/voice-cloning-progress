import asyncio
import edge_tts
import os

async def create_native_telugu_base():
    """Create Telugu audio with native pronunciation for voice cloning"""
    
    # Native Telugu text (proper script for native pronunciation)
    native_telugu_text = """
    అదే మరి, నీవు లినియర్ రిగ్రెషన్ చూసినప్పుడు, 
    అక్కడ మనం ఒక నంబర్ ప్రిడిక్ట్ చేయడానికి ప్రయత్నిస్తాము. 
    దానిని రిగ్రెషన్ ప్రాబ్లెమ్ అంటారు.
    """
    
    output_dir = "D:/Telugu/output"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        print("Creating native Telugu audio for voice cloning...")
        
        # Use Telugu male voice for native pronunciation
        communicate = edge_tts.Communicate(native_telugu_text.strip(), "te-IN-MohanNeural")
        await communicate.save(f"{output_dir}/native_telugu_for_voice_clone.wav")
        
        print("✓ Created: native_telugu_for_voice_clone.wav")
        print("This has proper Telugu pronunciation!")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def create_voice_cloning_instructions():
    """Create step-by-step voice cloning instructions"""
    
    instructions = """
NATIVE TELUGU + YOUR VOICE SOLUTION
==================================

STEP 1: ✓ COMPLETED
- Created native_telugu_for_voice_clone.wav
- Has proper Telugu pronunciation
- Uses Microsoft's Telugu voice

STEP 2: VOICE CLONING (Choose one method)

METHOD A: ELEVENLABS (EASIEST - 5 minutes)
1. Go to: https://elevenlabs.io
2. Sign up (free trial available)
3. Click "Voice Lab" → "Add Voice"
4. Upload: D:/Telugu/input/input_english.wav (your voice sample)
5. Name it: "My Voice"
6. Go to "Speech Synthesis"
7. Select your cloned voice
8. Upload the Telugu text or type:
   "అదే మరి, నీవు లినియర్ రిగ్రెషన్ చూసినప్పుడు, అక్కడ మనం ఒక నంబర్ ప్రిడిక్ట్ చేయడానికి ప్రయత్నిస్తాము. దానిని రిగ్రెషన్ ప్రాబ్లెమ్ అంటారు."
9. Generate → Download
RESULT: Perfect Telugu in YOUR voice!

METHOD B: RVC (FREE - 2-3 hours)
1. Train RVC model on your English voice
2. Convert native_telugu_for_voice_clone.wav to your voice
3. Result: Native Telugu pronunciation in your voice

METHOD C: SO-VITS-SVC (ADVANCED)
1. More complex but higher quality
2. Better voice similarity than RVC

RECOMMENDATION: Use ElevenLabs for immediate results!
"""
    
    with open("D:/Telugu/voice_cloning_native_telugu.txt", "w", encoding="utf-8") as f:
        f.write(instructions)
    
    print("Created: voice_cloning_native_telugu.txt")

async def main():
    print("NATIVE TELUGU + VOICE CLONING SOLUTION")
    print("=" * 45)
    
    # Step 1: Create native Telugu audio
    success = await create_native_telugu_base()
    
    if success:
        # Step 2: Create instructions
        create_voice_cloning_instructions()
        
        print("\n" + "=" * 45)
        print("SOLUTION READY!")
        print("1. ✓ Native Telugu audio created")
        print("2. ✓ Voice cloning instructions ready")
        print("\nNEXT: Follow voice_cloning_native_telugu.txt")
        print("RECOMMENDED: Use ElevenLabs for best results")
    else:
        print("Failed to create Telugu audio")

if __name__ == "__main__":
    asyncio.run(main())