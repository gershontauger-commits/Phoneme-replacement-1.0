"""
Test script for Hebrew Speech Correction System
Run this to verify all components are working
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import numpy as np
        print("✓ NumPy")
    except ImportError as e:
        print(f"✗ NumPy: {e}")
        return False
    
    try:
        import librosa
        print("✓ librosa")
    except ImportError as e:
        print(f"✗ librosa: {e}")
        return False
    
    try:
        import sounddevice as sd
        print("✓ sounddevice")
    except ImportError as e:
        print(f"✗ sounddevice: {e}")
        return False
    
    try:
        import soundfile as sf
        print("✓ soundfile")
    except ImportError as e:
        print(f"✗ soundfile: {e}")
        return False
    
    try:
        import torch
        print(f"✓ PyTorch {torch.__version__}")
    except ImportError as e:
        print(f"✗ PyTorch: {e}")
        return False
    
    try:
        from sklearn.metrics.pairwise import cosine_similarity
        print("✓ scikit-learn")
    except ImportError as e:
        print(f"✗ scikit-learn: {e}")
        return False
    
    try:
        import tkinter
        print("✓ tkinter")
    except ImportError as e:
        print(f"✗ tkinter: {e}")
        return False
    
    return True


def test_modules():
    """Test if our modules can be loaded"""
    print("\nTesting custom modules...")
    
    try:
        from src.audio_recorder import AudioRecorder
        print("✓ AudioRecorder")
    except Exception as e:
        print(f"✗ AudioRecorder: {e}")
        return False
    
    try:
        from src.syllable_analyzer import SyllableAnalyzer
        print("✓ SyllableAnalyzer")
    except Exception as e:
        print(f"✗ SyllableAnalyzer: {e}")
        return False
    
    try:
        from src.hebrew_syllables import get_syllable_list
        syllables = get_syllable_list()
        print(f"✓ Hebrew Syllables (loaded {len(syllables)} syllables)")
    except Exception as e:
        print(f"✗ Hebrew Syllables: {e}")
        return False
    
    try:
        from src.training_system import SyllableTrainingSystem
        print("✓ SyllableTrainingSystem")
    except Exception as e:
        print(f"✗ SyllableTrainingSystem: {e}")
        return False
    
    try:
        from src.pronunciation_model import PronunciationModel
        print("✓ PronunciationModel")
    except Exception as e:
        print(f"✗ PronunciationModel: {e}")
        return False
    
    try:
        from src.audio_corrector import AudioCorrector
        print("✓ AudioCorrector")
    except Exception as e:
        print(f"✗ AudioCorrector: {e}")
        return False
    
    return True


def test_audio_devices():
    """Test audio device availability"""
    print("\nTesting audio devices...")
    
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        print(f"✓ Found {len(devices)} audio device(s)")
        
        # Show default input device
        default_input = sd.query_devices(kind='input')
        print(f"  Default input: {default_input['name']}")
        
        return True
    except Exception as e:
        print(f"✗ Audio device test failed: {e}")
        return False


def test_directories():
    """Test if necessary directories exist"""
    print("\nTesting directories...")
    
    from config import DATA_DIR, MODELS_DIR, TRAINING_DATA_DIR, SYLLABLES_DIR, RECORDINGS_DIR
    
    dirs = {
        'Data': DATA_DIR,
        'Models': MODELS_DIR,
        'Training Data': TRAINING_DATA_DIR,
        'Syllables': SYLLABLES_DIR,
        'Recordings': RECORDINGS_DIR
    }
    
    all_exist = True
    for name, path in dirs.items():
        if os.path.exists(path):
            print(f"✓ {name}: {path}")
        else:
            print(f"✗ {name} missing: {path}")
            os.makedirs(path, exist_ok=True)
            print(f"  Created directory")
    
    return True


def test_feature_extraction():
    """Test feature extraction on synthetic audio"""
    print("\nTesting feature extraction...")
    
    try:
        import numpy as np
        from src.syllable_analyzer import SyllableAnalyzer
        
        # Create synthetic audio (1 second of sine wave)
        sample_rate = 22050
        duration = 1.0
        frequency = 440  # A4 note
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = np.sin(2 * np.pi * frequency * t)
        
        # Extract features
        analyzer = SyllableAnalyzer()
        features = analyzer.extract_features(audio)
        
        print(f"✓ Feature extraction successful")
        print(f"  Feature vector shape: {features.shape}")
        print(f"  Feature vector size: {len(features)} dimensions")
        
        return True
    except Exception as e:
        print(f"✗ Feature extraction failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Hebrew Speech Correction System - Test Suite")
    print("=" * 60)
    print()
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Modules", test_modules()))
    results.append(("Audio Devices", test_audio_devices()))
    results.append(("Directories", test_directories()))
    results.append(("Feature Extraction", test_feature_extraction()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! System is ready to use.")
        print("\nRun the application with: python main.py")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        print("You may need to install missing dependencies.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
