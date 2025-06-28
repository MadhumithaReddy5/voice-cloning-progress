# Telugu Voice Cloning System

A neural text-to-speech system for converting English audio to Telugu speech while preserving the original speaker's voice characteristics.

## Features

- **Speech Recognition**: Convert English audio to text
- **Translation**: English to Telugu translation
- **Voice Cloning**: Generate Telugu speech in original speaker's voice
- **Neural TTS**: Custom IndicF5 model for Telugu speech synthesis

## Setup

### Requirements
```bash
pip install -r requirements.txt
```

### GPU Setup (Recommended)
```bash
# Check CUDA version
nvidia-smi

# Install PyTorch with CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## Usage

### Training
```bash
python train_indicf5_telugu.py
```

### Generation
```bash
python generate_telugu_speech.py
```

### Voice Conversion
```bash
python voice_conversion.py
```

## Configuration

Edit `config.json` for training parameters:
- `batch_size`: Batch size for training
- `epochs`: Number of training epochs
- `learning_rate`: Learning rate
- `dataset_path`: Path to Telugu dataset

## Model Architecture

- **Text Encoder**: Transformer-based text encoding
- **Duration Predictor**: Predicts phoneme durations
- **Mel Decoder**: Generates mel spectrograms
- **Vocoder**: Converts mel to audio

## Dataset

Place your Telugu dataset in the following structure:
```
telugu_dataset/
├── metadata_with_speakers.csv
└── wavs/
    ├── audio1.wav
    ├── audio2.wav
    └── ...
```

## Results

The system can:
1. Convert English audio to Telugu text
2. Generate Telugu speech with voice characteristics preservation
3. Support colloquial Telugu expressions

## Training Progress

- **CPU Training**: ~2 hours per epoch (slow)
- **GPU Training**: ~5-10 minutes per epoch (recommended)
- **Recommended**: 200+ epochs for good quality

## Files

- `train_indicf5_telugu.py`: Main training script
- `generate_telugu_speech.py`: Text-to-speech generation
- `voice_conversion.py`: Voice cloning pipeline
- `vocoder.py`: Neural vocoder implementation
- `config.json`: Training configuration

## License

MIT License