import subprocess
import sys

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ {package} installed successfully")
    except Exception as e:
        print(f"✗ Failed to install {package}: {e}")

# Install missing RVC dependencies
packages = [
    "python-dotenv",
    "ffmpeg-python", 
    "av",
    "pyaudio",
    "sounddevice",
    "librosa==0.9.1",
    "numpy==1.23.5"
]

print("Installing RVC dependencies...")
for package in packages:
    install_package(package)

print("\nAll dependencies installed! Now try: python infer-web.py")