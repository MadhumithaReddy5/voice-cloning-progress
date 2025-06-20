
# RVC SETUP FOR VOICE CONVERSION
# Run these commands in order:

# 1. Create RVC directory
mkdir D:\Telugu\RVC
cd D:\Telugu\RVC

# 2. Download RVC
git clone https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI.git
cd Retrieval-based-Voice-Conversion-WebUI

# 3. Install requirements
pip install -r requirements.txt

# 4. Run RVC web interface
python infer-web.py

# 5. Open browser: http://localhost:7865
# 6. Train tab: Upload your English audio
# 7. Train model (1-2 hours)
# 8. Inference tab: Convert telugu_for_conversion.wav to your voice
