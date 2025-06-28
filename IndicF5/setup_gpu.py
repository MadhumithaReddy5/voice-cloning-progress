import torch
import subprocess
import sys

def check_gpu_setup():
    """Check GPU setup and provide installation commands"""
    
    print("=== GPU Setup Check ===")
    
    # Check CUDA availability
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"CUDA version: {torch.version.cuda}")
        print(f"GPU count: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
        print("✅ GPU setup is ready!")
        return True
    else:
        print("❌ CUDA not available")
        print("\n=== GPU Installation Instructions ===")
        
        # Check NVIDIA driver
        try:
            result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ NVIDIA driver detected")
                print("Install PyTorch with CUDA:")
                print("\nFor CUDA 11.8:")
                print("pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
                print("\nFor CUDA 12.1:")
                print("pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
            else:
                print("❌ NVIDIA driver not found")
                print("1. Install NVIDIA GPU drivers first")
                print("2. Install CUDA toolkit")
                print("3. Then install PyTorch with CUDA")
        except FileNotFoundError:
            print("❌ nvidia-smi not found")
            print("Install NVIDIA drivers and CUDA toolkit first")
        
        return False

def update_config_for_gpu():
    """Update config for GPU training"""
    import json
    
    config_path = "config.json"
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Update for GPU training
        if torch.cuda.is_available():
            config["batch_size"] = 16  # Larger batch size for GPU
            config["epochs"] = 500     # More epochs for better results
            config["save_every"] = 25  # Save less frequently
            
            print("Updated config for GPU training:")
            print(f"- Batch size: {config['batch_size']}")
            print(f"- Epochs: {config['epochs']}")
            print(f"- Save every: {config['save_every']} epochs")
        else:
            config["batch_size"] = 2   # Small batch for CPU
            config["epochs"] = 50      # Fewer epochs for CPU
            config["save_every"] = 10
            
            print("Updated config for CPU training:")
            print(f"- Batch size: {config['batch_size']}")
            print(f"- Epochs: {config['epochs']}")
        
        # Save updated config
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Config updated in {config_path}")
        
    except Exception as e:
        print(f"❌ Error updating config: {e}")

def install_requirements():
    """Install requirements based on GPU availability"""
    
    print("\n=== Installing Requirements ===")
    
    if torch.cuda.is_available():
        print("Installing for GPU setup...")
        # GPU requirements already installed if CUDA is available
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        print("Installing for CPU setup...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

if __name__ == "__main__":
    gpu_available = check_gpu_setup()
    update_config_for_gpu()
    
    print(f"\n=== Training Recommendations ===")
    if gpu_available:
        print("🚀 GPU detected - you can train with:")
        print("- Larger batch sizes (16+)")
        print("- More epochs (500+)")
        print("- Full dataset")
        print("- Expected training time: Hours instead of days")
    else:
        print("🐌 CPU only - training will be slow:")
        print("- Small batch sizes (2-4)")
        print("- Fewer epochs (50-100)")
        print("- Limited dataset")
        print("- Expected training time: Days/weeks")
    
    print(f"\nRun: python train_indicf5_telugu.py")