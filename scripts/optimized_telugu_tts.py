
import asyncio
import edge_tts
import os

async def create_optimized_telugu_audio():
    """Create the best possible Telugu audio with current tools"""
    
    # Optimized Telugu text with phonetic improvements
    telugu_optimized = """
    అదే మరి, నీవు లినియర్ రిగ్రెషన్ చూసినప్పుడు, 
    అక్కడ మనం ఒక నంబర్ ప్రిడిక్ట్ చేయడానికి ప్రయత్నిస్తాము. 
    దానిని రిగ్రెషన్ ప్రాబ్లెమ్ అంటారు.
    """
    
    # Use SSML for better control (commented out due to complexity)
    # ssml_text = "<speak>...</speak>"
    
    output_dir = "D:/Telugu/output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create optimized version
    communicate = edge_tts.Communicate(telugu_optimized, "te-IN-MohanNeural")
    await communicate.save(f"{output_dir}/optimized_telugu_final.wav")
    
    print("Optimized Telugu audio created: optimized_telugu_final.wav")
    
    # Also create phonetic version
    phonetic_text = "Ade mari, neevu linear regression choosinappudu, akkada manam oka number predict cheyadaniki prayatnistamu. Danini regression problem antaru."
    
    communicate2 = edge_tts.Communicate(phonetic_text, "te-IN-MohanNeural")
    await communicate2.save(f"{output_dir}/phonetic_telugu_final.wav")
    
    print("Phonetic Telugu audio created: phonetic_telugu_final.wav")

if __name__ == "__main__":
    asyncio.run(create_optimized_telugu_audio())
