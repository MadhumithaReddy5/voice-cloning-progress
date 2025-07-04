import pandas as pd
import os

# Load your CSV file (update path if needed)
df = pd.read_csv("metadata_with_speakers.csv")

# Open new metadata.txt file
with open("metadata.txt", "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        file_name = os.path.basename(row['audio_file'])  # Get filename only (remove folder path)
        text = row['text']
        speaker = row['speaker']
        
        line = f"{file_name}|{text}|{speaker}\n"
        f.write(line)

print("✅ metadata.txt generated successfully!")
