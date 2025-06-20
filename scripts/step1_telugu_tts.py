
import asyncio
import edge_tts
import os

async def create_telugu_audio():
    """Create Telugu audio with good pronunciation"""
    
    # Telugu text with mixed English (natural)
    telugu_text = """
    అదే మరి, నీవు linear regression చూసినప్పుడు, 
    అక్కడ మనం ఒక number predict చేయడానికి ప్రయత్నిస్తాము. 
    దానిని regression problem అంటారు.
    """
    
    output_dir = "D:/Telugu/output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create Telugu audio
    communicate = edge_tts.Communicate(telugu_text, "te-IN-MohanNeural")
    await communicate.save(f"{output_dir}/telugu_for_conversion.wav")
    
    print("Telugu audio created: telugu_for_conversion.wav")
    print("Next: Use RVC to convert this to your voice!")

if __name__ == "__main__":
    asyncio.run(create_telugu_audio())
