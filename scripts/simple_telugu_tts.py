import os
import sys

# Fix encoding for Windows
if sys.platform == "win32":
    os.system("chcp 65001")

def create_telugu_audio():
    print("=== SIMPLE TELUGU TTS ===")
    
    # Your English text (manually input to avoid Whisper issues)
    english_text = "On the other hand, when you have seen the linear regression, there we try to predict a number. That is called a regression problem."
    print(f"English: {english_text}")
    
    # Convert to colloquial Telugu with English mixing
    telugu_colloquial = "Ade mari, neevu linear regression choosinappudu, akkada manam oka number predict cheyadaniki prayatnistamu. Danini regression problem antaru."
    print(f"Telugu Colloquial: {telugu_colloquial}")
    
    # Generate Telugu audio
    output_path = "D:/Telugu/output/simple_telugu_audio.wav"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        import edge_tts
        import asyncio
        
        async def create_audio():
            voice = "te-IN-MohanNeural"  # Male Telugu voice
            communicate = edge_tts.Communicate(telugu_colloquial, voice)
            await communicate.save(output_path)
        
        asyncio.run(create_audio())
        print(f"SUCCESS: Telugu audio saved at {output_path}")
        
        # Also save text version
        with open(output_path.replace('.wav', '.txt'), 'w', encoding='utf-8') as f:
            f.write(f"English: {english_text}\n\n")
            f.write(f"Telugu Colloquial: {telugu_colloquial}\n\n")
            f.write("Voice: Microsoft Telugu Male (MohanNeural)\n")
        
        print("Audio generation completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        
        # Save text file as fallback
        text_path = output_path.replace('.wav', '.txt')
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(f"English: {english_text}\n\n")
            f.write(f"Telugu Colloquial: {telugu_colloquial}\n\n")
            f.write("Note: Audio generation failed, but text is saved.\n")
        
        print(f"Text saved at: {text_path}")
        return False

if __name__ == "__main__":
    create_telugu_audio()