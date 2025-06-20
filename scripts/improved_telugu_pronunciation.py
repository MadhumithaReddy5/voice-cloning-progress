import asyncio
import edge_tts
import os

async def create_improved_telugu_audio():
    """Create Telugu audio with improved pronunciation and clarity"""
    
    # Improved phonetic spellings for better pronunciation
    improved_versions = {
        "slow_clear": {
            "text": "Ah-dhey mah-ri, nee-vu linear regression choo-si-nap-pu-du, ak-ka-da mah-nam o-ka number predict chey-ya-daa-ni-ki pra-yat-nis-taa-mu. Dha-ni-ni regression problem an-taa-ru.",
            "voice": "te-IN-MohanNeural",
            "filename": "improved_slow_clear.wav"
        },
        
        "natural_flow": {
            "text": "Adhe mari, neevu linear regression choosinappudu, akkada manam oka number predict cheyadaniki prayatnistamu. Danini regression problem antaru.",
            "voice": "te-IN-MohanNeural", 
            "filename": "improved_natural_flow.wav"
        },
        
        "mixed_english": {
            "text": "అదే మరి, నీవు linear regression చూసినప్పుడు, అక్కడ మనం ఒక number predict చేయడానికి ప్రయత్నిస్తాము. దానిని regression problem అంటారు.",
            "voice": "te-IN-MohanNeural",
            "filename": "improved_mixed_english.wav"
        },
        
        "enhanced_phonetic": {
            "text": "Ah-dhe mah-ri, nee-vu linear regression choo-see-na-ppu-du, ak-ka-da mah-nam o-ka number predict chey-ya-daa-ni-ki pra-yat-nis-taa-mu. Dha-ni-ni regression problem an-taa-ru.",
            "voice": "te-IN-MohanNeural",
            "filename": "improved_enhanced_phonetic.wav"
        }
    }
    
    output_dir = "D:/Telugu/output"
    os.makedirs(output_dir, exist_ok=True)
    
    print("Creating improved Telugu audio versions...")
    
    for version_name, config in improved_versions.items():
        try:
            print(f"Generating: {version_name}")
            filepath = os.path.join(output_dir, config["filename"])
            
            communicate = edge_tts.Communicate(config["text"], config["voice"])
            await communicate.save(filepath)
            
            print(f"  ✓ Created: {config['filename']}")
            
        except Exception as e:
            print(f"  ✗ Failed {version_name}: {e}")
    
    # Also create with female voice for comparison
    try:
        print("Creating female voice version...")
        female_text = "Adhe mari, neevu linear regression choosinappudu, akkada manam oka number predict cheyadaniki prayatnistamu. Danini regression problem antaru."
        
        communicate = edge_tts.Communicate(female_text, "te-IN-ShrutiNeural")
        await communicate.save(os.path.join(output_dir, "improved_female_voice.wav"))
        
        print("  ✓ Created: improved_female_voice.wav")
        
    except Exception as e:
        print(f"  ✗ Female voice failed: {e}")

def create_pronunciation_guide():
    """Create a guide for better Telugu pronunciation"""
    
    guide = """
TELUGU PRONUNCIATION IMPROVEMENT GUIDE
=====================================

PROBLEM: Current phonetic Telugu has unclear pronunciation

SOLUTIONS CREATED:
1. improved_slow_clear.wav - Hyphenated for clarity
2. improved_natural_flow.wav - Natural phonetic flow  
3. improved_mixed_english.wav - Telugu script with English words
4. improved_enhanced_phonetic.wav - Enhanced phonetic spelling
5. improved_female_voice.wav - Female voice comparison

PRONUNCIATION TIPS:
- "Adhe" = "Ah-dhe" (not "Add-he")
- "mari" = "mah-ri" (not "marry") 
- "choosinappudu" = "choo-see-na-ppu-du"
- "akkada" = "ak-ka-da" (clear syllables)
- "manam" = "mah-nam" (not "man-am")
- "cheyadaniki" = "chey-ya-daa-ni-ki"
- "prayatnistamu" = "pra-yat-nis-taa-mu"
- "danini" = "dha-ni-ni" (soft 'dh')
- "antaru" = "an-taa-ru"

NEXT STEPS:
1. Listen to all 5 versions
2. Choose the clearest one
3. Use that as base for voice cloning with RVC
"""
    
    with open("D:/Telugu/pronunciation_guide.txt", "w", encoding="utf-8") as f:
        f.write(guide)
    
    print("Created: pronunciation_guide.txt")

async def main():
    print("IMPROVING TELUGU PRONUNCIATION")
    print("=" * 40)
    
    await create_improved_telugu_audio()
    create_pronunciation_guide()
    
    print("\n" + "=" * 40)
    print("IMPROVEMENT COMPLETE!")
    print("Check D:/Telugu/output/ for 5 improved versions")
    print("Listen to each and choose the clearest one")
    print("Then use RVC to convert to your voice")

if __name__ == "__main__":
    asyncio.run(main())