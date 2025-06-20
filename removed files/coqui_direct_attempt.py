
# After fixing environment, try this:

import torch
from TTS.api import TTS

# Fix PyTorch loading
torch.serialization.add_safe_globals([
    'TTS.tts.configs.xtts_config.XttsConfig'
])

# Load XTTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

# Try Telugu phonetic spelling
telugu_phonetic = "Ade mari, neevu linear regression choosinappudu, akkada manam oka number predict cheyadaniki prayatnistamu."

# Generate with your voice
tts.tts_to_file(
    text=telugu_phonetic,
    speaker_wav="D:/Telugu/input/input_english.wav",
    language="en",  # Use English model for phonetic Telugu
    file_path="D:/Telugu/output/coqui_telugu.wav"
)
