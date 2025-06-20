
import asyncio
import edge_tts
import os

async def create_audio():
    # Telugu text with natural English mixing
    telugu_text = """
    అదే మరి, నీవు linear regression చూసినప్పుడు, 
    అక్కడ మనం ఒక number predict చేయడానికి ప్రయత్నిస్తాము. 
    దానిని regression problem అంటారు.
    """
    
    output_dir = "D:/Telugu/output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create Telugu audio for conversion
    communicate = edge_tts.Communicate(telugu_text, "te-IN-MohanNeural")
    await communicate.save(f"{output_dir}/telugu_base_for_rvc.wav")
    
    print("Telugu base audio created: telugu_base_for_rvc.wav")
    print("This will be converted to your voice using RVC")

if __name__ == "__main__":
    asyncio.run(create_audio())
