@echo off
echo Installing RVC dependencies...

pip install python-dotenv
pip install ffmpeg-python
pip install av
pip install pyaudio
pip install sounddevice

echo.
echo Dependencies installed! Now try running RVC:
echo cd Retrieval-based-Voice-Conversion-WebUI
echo python infer-web.py
pause