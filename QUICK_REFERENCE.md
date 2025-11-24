# Quick Reference Guide - Hebrew Speech Correction System

## 🚀 Quick Commands

### Initial Setup (One-time)
```bash
cd /home/gershon-tauger/phoneme-replacement
chmod +x setup.sh
./setup.sh
source venv/bin/activate
```

### Daily Usage
```bash
# Activate environment
cd /home/gershon-tauger/phoneme-replacement
source venv/bin/activate

# Run main application
python main.py

# OR run quick start menu
python quickstart.py
```

### Testing
```bash
# Test all components
python test_system.py

# Test individual modules
python src/audio_recorder.py
python src/syllable_analyzer.py
python src/hebrew_syllables.py
```

---

## 📁 File Reference

### Main Files
- `main.py` - **Main GUI application** (Start here!)
- `quickstart.py` - Quick testing and demos
- `config.py` - All configuration settings
- `requirements.txt` - Python dependencies

### Core Modules (`src/`)
- `audio_recorder.py` - Records audio from microphone
- `syllable_analyzer.py` - Detects and analyzes syllables
- `hebrew_syllables.py` - 100 Hebrew syllables database
- `training_system.py` - Manages training recordings
- `pronunciation_model.py` - ML model for assessment
- `audio_corrector.py` - Corrects mispronunciations

### Documentation
- `README.md` - User manual and installation guide
- `PROJECT_SUMMARY.md` - Technical overview
- `QUICK_REFERENCE.md` - This file!

### Utilities
- `setup.sh` - Automated setup script
- `test_system.py` - System verification
- `.gitignore` - Git ignore rules

---

## 🎯 Common Tasks

### First Time Setup
1. Run `./setup.sh`
2. Activate venv: `source venv/bin/activate`
3. Test: `python test_system.py`
4. Launch: `python main.py`

### Training Syllables
1. Launch: `python main.py`
2. Select "Training Mode"
3. Record each displayed syllable
4. Progress bar shows completion

### Correcting Speech
1. Launch: `python main.py`
2. Select "Correction Mode"
3. Click "Start Recording"
4. Speak Hebrew sentences
5. Click "Stop Recording"
6. Click "Analyze & Correct"
7. Review results and play audio

### Checking System Status
```bash
python quickstart.py
# Choose option 3 - System Information
```

### Viewing Syllable Database
```bash
python quickstart.py
# Choose option 2 - Show Syllable Database
```

---

## ⚙️ Configuration Quick Reference

Edit `config.py` to change:

### Audio Settings
```python
SAMPLE_RATE = 22050        # Audio quality (Hz)
CHANNELS = 1               # Mono/Stereo
```

### Syllable Settings
```python
TARGET_SYLLABLE_COUNT = 100           # Number of syllables
MIN_SYLLABLE_DURATION = 0.1           # Minimum length (seconds)
MAX_SYLLABLE_DURATION = 0.5           # Maximum length (seconds)
```

### ML Settings
```python
EMBEDDING_DIM = 128                   # Model embedding size
SIMILARITY_THRESHOLD = 0.85           # Quality threshold (0-1)
```

### Training Settings
```python
BATCH_SIZE = 32
LEARNING_RATE = 0.001
EPOCHS = 50
```

---

## 🐛 Troubleshooting Quick Fixes

### "No module named 'sounddevice'"
```bash
pip install sounddevice soundfile
# On Ubuntu/Debian:
sudo apt-get install portaudio19-dev python3-pyaudio
```

### "No audio devices found"
```bash
# Check devices
python -c "import sounddevice as sd; print(sd.query_devices())"

# Check microphone permissions
# Linux: Check ALSA/PulseAudio settings
# Make sure microphone is not muted
```

### "Import librosa failed"
```bash
pip install librosa
# May need: sudo apt-get install ffmpeg
```

### "PyTorch not found"
```bash
# CPU version
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# GPU version (CUDA)
pip install torch torchvision torchaudio
```

### GUI doesn't start
```bash
# Check tkinter
python -c "import tkinter; print('OK')"

# Install if needed (Ubuntu/Debian)
sudo apt-get install python3-tk
```

### Permission denied on setup.sh
```bash
chmod +x setup.sh
./setup.sh
```

---

## 📊 Data Locations

### Recordings
- Original recordings: `data/recordings/recording_YYYYMMDD_HHMMSS.wav`
- Corrected audio: `data/recordings/corrected_YYYYMMDD_HHMMSS.wav`

### Training Data
- Syllable recordings: `data/syllables/[syllable_name]/`
- Training progress: `data/training_data/training_progress.json`
- Feature data: `data/training_data/syllable_features.npz`

### Models
- Trained model: `models/pronunciation_model.pth`

---

## 🎨 GUI Guide

### Training Mode Layout
```
┌─────────────────────────────────────────┐
│  Hebrew Speech Correction System        │
├─────────────────────────────────────────┤
│ ⚪ Training Mode  ⚪ Correction Mode     │
├─────────────────────────────────────────┤
│  Training Progress: 15/100 (15%)        │
│  [████░░░░░░░░░░░░░░░░░░░░░░░░░░]       │
│                                         │
│         Current Syllable:               │
│              בְּ                        │
│                                         │
│  [Start Recording] [Stop & Save] [Next] │
└─────────────────────────────────────────┘
```

### Correction Mode Layout
```
┌─────────────────────────────────────────┐
│  Hebrew Speech Correction System        │
├─────────────────────────────────────────┤
│ ⚪ Training Mode  ⚪ Correction Mode     │
├─────────────────────────────────────────┤
│  Record Hebrew speech for analysis      │
│                                         │
│  [Start] [Stop] [Analyze & Correct]     │
│                                         │
│  ┌─── Analysis Results ───────────────┐ │
│  │ Total syllables: 12                │ │
│  │ Corrected: 3                       │ │
│  │ Quality score: 0.82                │ │
│  │                                    │ │
│  │ Details: ...                       │ │
│  └────────────────────────────────────┘ │
│                                         │
│  [Play Original] [Play Corrected] [Save]│
└─────────────────────────────────────────┘
```

---

## 📖 Python API Quick Reference

### Recording Audio
```python
from src.audio_recorder import AudioRecorder

recorder = AudioRecorder()
recorder.start_recording()
# ... speak ...
audio = recorder.stop_recording()
recorder.save_recording(audio, "myfile.wav")
```

### Analyzing Syllables
```python
from src.syllable_analyzer import SyllableAnalyzer

analyzer = SyllableAnalyzer()
syllables = analyzer.analyze_file("audio.wav")
for syl in syllables:
    print(f"Time: {syl['start_time']:.2f}s")
```

### Training System
```python
from src.training_system import SyllableTrainingSystem

trainer = SyllableTrainingSystem()
status = trainer.get_training_status()
print(f"Trained: {status['trained']}/{status['total']}")
```

### Pronunciation Model
```python
from src.pronunciation_model import PronunciationModel

model = PronunciationModel()
model.load_model("models/pronunciation_model.pth")
assessment = model.assess_pronunciation(features, "בְּ")
print(f"Quality: {assessment['quality_score']}")
```

### Audio Correction
```python
from src.audio_corrector import AudioCorrector

corrector = AudioCorrector(model, trainer)
corrected_audio, report = corrector.correct_audio(audio)
corrector.save_corrected_audio(corrected_audio)
```

---

## 🔗 Useful Links

### Documentation
- Full README: `README.md`
- Project Summary: `PROJECT_SUMMARY.md`
- This guide: `QUICK_REFERENCE.md`

### Dependencies
- librosa: https://librosa.org/
- PyTorch: https://pytorch.org/
- sounddevice: https://python-sounddevice.readthedocs.io/

### Support
- Check `test_system.py` output for diagnostics
- Review `config.py` for settings
- Run `python quickstart.py` for interactive help

---

## ✅ Quick Checklist

Before first use:
- [ ] Python 3.8+ installed
- [ ] Ran `./setup.sh` successfully
- [ ] Virtual environment activated
- [ ] `python test_system.py` passes all tests
- [ ] Microphone connected and working
- [ ] `python main.py` launches GUI

For good results:
- [ ] Train at least 20 syllables
- [ ] Record in quiet environment
- [ ] Speak clearly and at normal pace
- [ ] Keep consistent microphone distance
- [ ] Check quality scores in results

---

## 🎯 Performance Tips

### Better Training
- Record multiple samples per syllable
- Use high-quality microphone
- Record in quiet room
- Speak at normal conversational speed
- Pronounce syllables clearly

### Better Correction
- Ensure adequate training first (20+ syllables)
- Record clear audio with minimal background noise
- Speak at normal pace (not too fast/slow)
- Keep consistent volume
- Review and retrain problem syllables

### Optimization
- Lower `SAMPLE_RATE` for faster processing
- Adjust `SIMILARITY_THRESHOLD` for strictness
- Increase `EPOCHS` for better model
- Use GPU if available (PyTorch will auto-detect)

---

**Last Updated**: November 13, 2025
**Version**: 1.0
**Project**: Hebrew Speech Correction System
