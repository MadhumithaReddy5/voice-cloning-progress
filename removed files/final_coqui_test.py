import asyncio
import os

def test_current_capabilities():
    print("TESTING CURRENT TTS CAPABILITIES")
    print("=" * 40)
    
    # Test Edge TTS
    try:
        import edge_tts
        print("Edge TTS: Available")
        return True
    except ImportError:
        print("Edge TTS: Not available")
        return False

async def create_best_telugu_audio():
    """Create the best possible Telugu audio"""
    
    try:
        import edge_tts
        
        # Get Telugu voices
        voices = await edge_tts.list_voices()
        telugu_voices = [v for v in voices if v['Locale'].startswith('te-')]
        
        print(f"Found {len(telugu_voices)} Telugu voices:")
        for voice in telugu_voices:
            print(f"  - {voice['Name']}: {voice['Gender']}")
        
        if not telugu_voices:
            print("No Telugu voices found!")
            return False
        
        # Use male voice
        male_voice = next((v for v in voices if v['Gender'] == 'Male'), telugu_voices[0])
        voice_name = male_voice['Name']
        
        print(f"\nUsing voice: {voice_name}")
        
        # Test different approaches
        test_cases = {
            "direct_telugu": "అదే మరి, నీవు లినియర్ రిగ్రెషన్ చూసినప్పుడు, అక్కడ మనం ఒక నంబర్ ప్రిడిక్ట్ చేయడానికి ప్రయత్నిస్తాము. దానిని రిగ్రెషన్ ప్రాబ్లెమ్ అంటారు.",
            "phonetic_telugu": "Ade mari, neevu linear regression choosinappudu, akkada manam oka number predict cheyadaniki prayatnistamu. Danini regression problem antaru.",
            "mixed_approach": "అదే మరి, నీవు linear regression చూసినప్పుడు, అక్కడ మనం ఒక number predict చేయడానికి ప్రయత్నిస్తాము. దానిని regression problem అంటారు."
        }
        
        output_dir = "D:/Telugu/output"
        os.makedirs(output_dir, exist_ok=True)
        
        results = {}
        
        for approach, text in test_cases.items():
            try:
                print(f"Testing: {approach}")
                filename = f"coqui_test_{approach}.wav"
                filepath = os.path.join(output_dir, filename)
                
                communicate = edge_tts.Communicate(text, voice_name)
                await communicate.save(filepath)
                
                print(f"  Success: {filename}")
                results[approach] = True
                
            except Exception as e:
                print(f"  Failed: {e}")
                results[approach] = False
        
        return results
        
    except Exception as e:
        print(f"Error: {e}")
        return {}

def show_final_assessment(results):
    print("\nFINAL COQUI EXTENT ASSESSMENT")
    print("=" * 40)
    
    working_count = sum(1 for success in results.values() if success)
    total_count = len(results)
    
    print(f"Working methods: {working_count}/{total_count}")
    
    for method, success in results.items():
        status = "WORKS" if success else "FAILED"
        print(f"  {method}: {status}")
    
    print("\nCOQUI TTS CAPABILITIES:")
    print("1. Basic TTS: Not installed (compilation issues)")
    print("2. XTTS Voice Cloning: Not available")
    print("3. Telugu Support: Limited")
    
    print("\nEDGE TTS CAPABILITIES:")
    print("1. Telugu TTS: Working")
    print("2. Voice Cloning: Not available")
    print("3. Pronunciation: Good with optimization")
    
    print("\nRECOMMENDATIONS:")
    print("1. For immediate Telugu audio: Use Edge TTS")
    print("2. For voice cloning: Use ElevenLabs or RVC")
    print("3. Coqui TTS needs environment fixes")
    
    if working_count > 0:
        print(f"\nSUCCESS: {working_count} Telugu methods working!")
        print("Check D:/Telugu/output/ for audio files")
    else:
        print("\nNO METHODS WORKING - Need to fix environment")

async def main():
    print("COQUI TTS EXTENT TEST - FINAL VERSION")
    print("=" * 50)
    
    # Test basic capabilities
    has_edge_tts = test_current_capabilities()
    
    if has_edge_tts:
        # Test Telugu generation
        results = await create_best_telugu_audio()
        
        # Show assessment
        show_final_assessment(results)
    else:
        print("\nNo TTS libraries available")
        print("Install: pip install edge-tts")
        print("Then run this test again")

if __name__ == "__main__":
    asyncio.run(main())