"""
Real-time audio recording module for Hebrew speech
"""
import sounddevice as sd
import soundfile as sf
import numpy as np
import queue
import threading
from datetime import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SAMPLE_RATE, CHANNELS, RECORDINGS_DIR


class AudioRecorder:
    """
    Handles real-time audio recording with start/stop functionality
    """
    
    def __init__(self, sample_rate=SAMPLE_RATE, channels=CHANNELS):
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = False
        self.audio_queue = queue.Queue()
        self.recorded_data = []
        
        # Ensure recordings directory exists
        os.makedirs(RECORDINGS_DIR, exist_ok=True)
    
    def _audio_callback(self, indata, frames, time_info, status):
        """Callback function for audio stream"""
        if status:
            print(f"Audio status: {status}")
        if self.recording:
            self.audio_queue.put(indata.copy())
    
    def start_recording(self):
        """Start recording audio"""
        if self.recording:
            print("Already recording!")
            return
        
        self.recording = True
        self.recorded_data = []
        
        # Start audio stream
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=self._audio_callback
        )
        self.stream.start()
        
        # Start thread to collect audio data
        self.record_thread = threading.Thread(target=self._collect_audio)
        self.record_thread.start()
        
        print("Recording started...")
    
    def _collect_audio(self):
        """Collect audio data from queue"""
        while self.recording:
            try:
                data = self.audio_queue.get(timeout=0.1)
                self.recorded_data.append(data)
            except queue.Empty:
                continue
    
    def stop_recording(self):
        """Stop recording and return the recorded audio"""
        if not self.recording:
            print("Not currently recording!")
            return None
        
        self.recording = False
        
        # Wait for collection thread to finish (with timeout)
        if hasattr(self, 'record_thread') and self.record_thread.is_alive():
            self.record_thread.join(timeout=2.0)  # Wait max 2 seconds
            if self.record_thread.is_alive():
                print("Warning: Recording thread did not finish in time")
        
        # Stop and close stream
        if hasattr(self, 'stream'):
            try:
                self.stream.stop()
                self.stream.close()
            except Exception as e:
                print(f"Error closing stream: {e}")
        
        # Combine all recorded chunks
        if self.recorded_data:
            try:
                audio_data = np.concatenate(self.recorded_data, axis=0)
                print(f"Recording stopped. Captured {len(audio_data)} samples.")
                return audio_data
            except Exception as e:
                print(f"Error concatenating audio data: {e}")
                return None
        else:
            print("No audio data recorded.")
            return None
    
    def save_recording(self, audio_data, filename=None):
        """Save recorded audio to file"""
        if audio_data is None or len(audio_data) == 0:
            print("No audio data to save.")
            return None
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}.wav"
        
        filepath = os.path.join(RECORDINGS_DIR, filename)
        sf.write(filepath, audio_data, self.sample_rate)
        print(f"Audio saved to: {filepath}")
        return filepath
    
    def is_recording(self):
        """Check if currently recording"""
        return self.recording


if __name__ == "__main__":
    # Test the recorder
    import time
    
    recorder = AudioRecorder()
    
    print("Starting 5-second test recording...")
    recorder.start_recording()
    time.sleep(5)
    audio = recorder.stop_recording()
    
    if audio is not None:
        filepath = recorder.save_recording(audio)
        print(f"Test recording saved successfully: {filepath}")
