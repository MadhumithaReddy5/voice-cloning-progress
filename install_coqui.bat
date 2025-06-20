@echo off
echo Installing Coqui TTS with Telugu support...

REM Fix encoding
chcp 65001

REM Install required packages
pip install --upgrade pip
pip install TTS
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install soundfile
pip install numpy==1.24.3

echo.
echo ✅ Installation complete!
echo Run: python coqui_telugu_fix.py
pause