# Requirements

This folder contains dependency files for the Audio Cloning Project.

## Installation

### Basic Installation
```bash
pip install -r requirements/requirements.txt
```

### Development Installation
```bash
pip install -r requirements/requirements-dev.txt
```

## Dependencies

- **torch**: PyTorch for deep learning operations
- **openai-whisper**: Speech-to-text transcription
- **TTS**: Text-to-speech synthesis with voice cloning
- **transformers**: Hugging Face transformers for tokenization
- **deep-translator**: Google Translate API wrapper
- **pydub**: Audio processing and manipulation
- **numpy/scipy**: Numerical computing
- **librosa/soundfile**: Audio analysis and I/O

## System Requirements

- Python 3.8+
- FFmpeg (for audio processing)
- CUDA-compatible GPU (recommended for faster processing)