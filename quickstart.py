"""
Quick start script for Hebrew Speech Correction System
Provides a simple command-line interface to test the system
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.audio_recorder import AudioRecorder
from src.syllable_analyzer import SyllableAnalyzer
from src.hebrew_syllables import get_syllable_list


def record_and_analyze():
    """Quick test: record audio and analyze syllables"""
    print("=" * 60)
    print("Quick Start - Record and Analyze")
    print("=" * 60)
    print()
    
    # Initialize components
    recorder = AudioRecorder()
    analyzer = SyllableAnalyzer()
    
    # Recording
    print("Recording will start in 3 seconds...")
    print("Speak a Hebrew sentence clearly.")
    print()
    
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    print("\n🎤 RECORDING NOW! (5 seconds)")
    recorder.start_recording()
    time.sleep(5)
    audio = recorder.stop_recording()
    
    if audio is None or len(audio) == 0:
        print("❌ No audio recorded. Check your microphone.")
        return
    
    # Save recording
    filepath = recorder.save_recording(audio, "quickstart_test.wav")
    print(f"✓ Recording saved: {filepath}")
    
    # Analyze
    print("\n🔍 Analyzing syllables...")
    syllables = analyzer.analyze_audio(audio)
    
    print(f"\n📊 Analysis Results:")
    print(f"   Detected {len(syllables)} syllables")
    print()
    
    for i, syllable in enumerate(syllables, 1):
        print(f"   {i}. Time: {syllable['start_time']:.2f}s - {syllable['end_time']:.2f}s")
        print(f"      Duration: {syllable['duration']:.2f}s")
        print(f"      Features: {len(syllable['features'])} dimensions")
    
    print("\n✓ Analysis complete!")
    print("\nTo use the full GUI application, run: python main.py")


def show_syllable_database():
    """Display the Hebrew syllable database"""
    print("=" * 60)
    print("Hebrew Syllable Database")
    print("=" * 60)
    print()
    
    syllables = get_syllable_list()
    
    print(f"Total syllables: {len(syllables)}")
    print()
    print("Sample syllables (first 20):")
    
    for i, syl in enumerate(syllables[:20], 1):
        print(f"  {i:2d}. {syl}")
    
    print(f"\n... and {len(syllables) - 20} more syllables")
    print()


def show_system_info():
    """Display system information"""
    print("=" * 60)
    print("System Information")
    print("=" * 60)
    print()
    
    # Check audio devices
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        
        print(f"Audio Devices: {len(devices)} found")
        default_input = sd.query_devices(kind='input')
        print(f"Default Input: {default_input['name']}")
        print()
    except Exception as e:
        print(f"Audio devices: Error - {e}")
        print()
    
    # Check configuration
    from config import (SAMPLE_RATE, TARGET_SYLLABLE_COUNT, 
                       SIMILARITY_THRESHOLD, EMBEDDING_DIM)
    
    print("Configuration:")
    print(f"  Sample Rate: {SAMPLE_RATE} Hz")
    print(f"  Target Syllables: {TARGET_SYLLABLE_COUNT}")
    print(f"  Similarity Threshold: {SIMILARITY_THRESHOLD}")
    print(f"  Embedding Dimensions: {EMBEDDING_DIM}")
    print()
    
    # Check directories
    from config import DATA_DIR, MODELS_DIR, RECORDINGS_DIR
    
    print("Directories:")
    print(f"  Data: {DATA_DIR}")
    print(f"  Models: {MODELS_DIR}")
    print(f"  Recordings: {RECORDINGS_DIR}")
    print()


def main_menu():
    """Main menu for quick start"""
    while True:
        print("\n" + "=" * 60)
        print("Hebrew Speech Correction System - Quick Start")
        print("=" * 60)
        print()
        print("1. Record and Analyze Test")
        print("2. Show Hebrew Syllable Database")
        print("3. Show System Information")
        print("4. Launch Full GUI Application")
        print("5. Exit")
        print()
        
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == "1":
            print()
            record_and_analyze()
        elif choice == "2":
            print()
            show_syllable_database()
        elif choice == "3":
            print()
            show_system_info()
        elif choice == "4":
            print("\nLaunching GUI application...")
            import main
            main.main()
            break
        elif choice == "5":
            print("\nGoodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please enter 1-5.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure all dependencies are installed:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
