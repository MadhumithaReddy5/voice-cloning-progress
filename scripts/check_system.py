#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
System Requirements Checker
"""

import psutil
import torch
import platform

def check_system_requirements():
    print("SYSTEM REQUIREMENTS CHECK")
    print("=" * 40)
    
    # RAM Check
    ram_gb = psutil.virtual_memory().total / (1024**3)
    ram_available = psutil.virtual_memory().available / (1024**3)
    
    print(f"💾 Total RAM: {ram_gb:.1f} GB")
    print(f"💾 Available RAM: {ram_available:.1f} GB")
    
    # GPU Check
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        print(f"🎮 GPU: {gpu_name}")
        print(f"🎮 GPU Memory: {gpu_memory:.1f} GB")
    else:
        print("🎮 GPU: Not available (CPU only)")
    
    # OS Check
    print(f"💻 OS: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {platform.python_version()}")
    
    print("\nRECOMMENDATIONS:")
    print("=" * 40)
    
    if ram_gb >= 12:
        print("✅ EXCELLENT: Can run full voice cloning locally")
        print("   - Use local setup with XTTS")
        print("   - High quality voice cloning")
    elif ram_gb >= 8:
        print("🟡 GOOD: Can run optimized voice cloning")
        print("   - Use smaller models")
        print("   - May need to close other apps")
    elif ram_gb >= 6:
        print("🟠 LIMITED: Basic TTS only")
        print("   - Use Google Colab for voice cloning")
        print("   - Local fallback to gTTS")
    else:
        print("🔴 INSUFFICIENT: Use Google Colab")
        print("   - Your system can't handle voice cloning")
        print("   - Google Colab is your best option")
    
    print(f"\n🎯 BEST OPTION FOR YOU:")
    if ram_gb >= 10:
        print("   Try local setup first, fallback to Colab")
    else:
        print("   Use Google Colab (FREE and more powerful)")

if __name__ == "__main__":
    check_system_requirements()