
# RVC Voice Cloning Setup Script
# Run this in Command Prompt

# Step 1: Create RVC directory
mkdir D:\Telugu\RVC
cd D:\Telugu\RVC

# Step 2: Download RVC
git clone https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI.git
cd Retrieval-based-Voice-Conversion-WebUI

# Step 3: Install requirements
pip install -r requirements.txt

# Step 4: Run RVC
python infer-web.py

# Step 5: Open browser to http://localhost:7865
# Step 6: Upload your English audio in "Train" tab
# Step 7: Train model (takes 1-2 hours)
# Step 8: Use "Inference" tab to convert Telugu TTS to your voice
