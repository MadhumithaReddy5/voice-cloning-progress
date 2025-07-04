input_metadata = "D:/Hindi Output/telugu_dataset/metadata.txt"
output_metadata = "D:/Hindi Output/telugu_dataset/metadata_1000_cleaned.txt"

# Consistent speaker name
final_speaker_label = "speaker1"

with open(input_metadata, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Take first 1000 lines
selected_lines = lines[:1001]

# Clean speaker labels
cleaned_lines = []
for line in selected_lines:
    parts = line.strip().split("|")
    if len(parts) == 3:
        filename, text, speaker = parts
        speaker = final_speaker_label
        cleaned_lines.append(f"{filename}|{text}|{speaker}\n")

# Save new cleaned metadata
with open(output_metadata, "w", encoding="utf-8") as f:
    f.writelines(cleaned_lines)

print("✅ Metadata cleaned and saved as metadata_1000_cleaned.txt")
