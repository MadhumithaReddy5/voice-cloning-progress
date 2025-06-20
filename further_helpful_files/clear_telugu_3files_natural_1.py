import asyncio
import edge_tts
import os

async def create_clear_telugu_audio():
    """Create clear Telugu audio with better pronunciation"""
    
    # Different pronunciation approaches
    versions = {
        "hyphenated": "Ah-dhe mah-ri, nee-vu linear regression choo-si-nap-pu-du, ak-ka-da mah-nam o-ka number predict chey-ya-daa-ni-ki pra-yat-nis-taa-mu. Dha-ni-ni regression problem an-taa-ru.",
        
        "natural": "Adhe mari, neevu linear regression choosinappudu, akkada manam oka number predict cheyadaniki prayatnistamu. Danini regression problem antaru.",
        
        "enhanced": "Ah-dhe mah-ri, nee-vu linear regression choo-see-na-ppu-du, ak-ka-da mah-nam o-ka number predict chey-ya-daa-ni-ki pra-yat-nis-taa-mu. Dha-ni-ni regression problem an-taa-ru."
    }
    
    output_dir = "D:/Telugu/output"
    os.makedirs(output_dir, exist_ok=True)
    
    print("Creating clear Telugu audio...")
    
    for name, text in versions.items():
        try:
            print(f"Creating: {name}")
            filename = f"clear_{name}.wav"
            filepath = os.path.join(output_dir, filename)
            
            communicate = edge_tts.Communicate(text, "te-IN-MohanNeural")
            await communicate.save(filepath)
            
            print(f"  Success: {filename}")
            
        except Exception as e:
            print(f"  Failed: {e}")
    
    print("\nAudio files created in D:/Telugu/output/")
    print("Listen to:")
    print("- clear_hyphenated.wav (slowest, clearest)")
    print("- clear_natural.wav (natural flow)")  
    print("- clear_enhanced.wav (enhanced clarity)")

if __name__ == "__main__":
    asyncio.run(create_clear_telugu_audio())