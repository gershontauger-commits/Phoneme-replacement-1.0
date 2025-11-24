"""
Hebrew syllable analyzer for audio processing
Detects and extracts syllables from Hebrew speech
"""
import numpy as np
import librosa
import soundfile as sf
from scipy import signal
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SAMPLE_RATE, MIN_SYLLABLE_DURATION, MAX_SYLLABLE_DURATION
from src.hebrew_syllables import COMMON_HEBREW_SYLLABLES


class SyllableAnalyzer:
    """
    Analyzes audio to detect and extract Hebrew syllables
    """
    
    def __init__(self, sample_rate=SAMPLE_RATE):
        self.sample_rate = sample_rate
        self.min_syllable_duration = MIN_SYLLABLE_DURATION
        self.max_syllable_duration = MAX_SYLLABLE_DURATION
    
    def load_audio(self, audio_path):
        """Load audio file"""
        audio, sr = librosa.load(audio_path, sr=self.sample_rate)
        return audio, sr
    
    def detect_syllable_boundaries(self, audio):
        """
        Detect syllable boundaries in audio using energy and onset detection
        Returns list of (start_time, end_time) tuples
        """
        # Calculate energy envelope
        hop_length = 512
        energy = librosa.feature.rms(y=audio, hop_length=hop_length)[0]
        
        # Calculate onset strength
        onset_env = librosa.onset.onset_strength(y=audio, sr=self.sample_rate, hop_length=hop_length)
        
        # Detect onsets (potential syllable starts)
        onsets = librosa.onset.onset_detect(
            onset_envelope=onset_env,
            sr=self.sample_rate,
            hop_length=hop_length,
            backtrack=True
        )
        
        # Convert onset frames to time
        onset_times = librosa.frames_to_time(onsets, sr=self.sample_rate, hop_length=hop_length)
        
        # Create syllable boundaries
        boundaries = []
        for i in range(len(onset_times) - 1):
            start = onset_times[i]
            end = onset_times[i + 1]
            duration = end - start
            
            # Filter by duration constraints
            if self.min_syllable_duration <= duration <= self.max_syllable_duration:
                boundaries.append((start, end))
        
        # Handle last syllable
        if len(onset_times) > 0:
            last_start = onset_times[-1]
            last_end = len(audio) / self.sample_rate
            if self.min_syllable_duration <= (last_end - last_start) <= self.max_syllable_duration:
                boundaries.append((last_start, last_end))
        
        return boundaries
    
    def extract_syllables(self, audio, boundaries):
        """
        Extract audio segments for each detected syllable
        Returns list of audio arrays
        """
        syllables = []
        for start_time, end_time in boundaries:
            start_sample = int(start_time * self.sample_rate)
            end_sample = int(end_time * self.sample_rate)
            syllable_audio = audio[start_sample:end_sample]
            syllables.append({
                'audio': syllable_audio,
                'start_time': start_time,
                'end_time': end_time,
                'duration': end_time - start_time
            })
        return syllables
    
    def extract_features(self, audio_segment):
        """
        Extract acoustic features from a syllable for comparison
        Returns feature vector
        """
        # MFCC features (Mel-frequency cepstral coefficients)
        mfccs = librosa.feature.mfcc(y=audio_segment, sr=self.sample_rate, n_mfcc=13)
        mfccs_mean = np.mean(mfccs, axis=1)
        mfccs_std = np.std(mfccs, axis=1)
        
        # Spectral features
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio_segment, sr=self.sample_rate))
        spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=audio_segment, sr=self.sample_rate))
        
        # Zero crossing rate
        zcr = np.mean(librosa.feature.zero_crossing_rate(audio_segment))
        
        # Combine features - ensure all are 1D arrays
        features = np.concatenate([
            mfccs_mean.flatten(),
            mfccs_std.flatten(),
            np.array([spectral_centroid, spectral_rolloff, zcr])
        ])
        
        return features
    
    def analyze_audio(self, audio):
        """
        Full analysis pipeline: detect syllables and extract features
        """
        # Detect syllable boundaries
        boundaries = self.detect_syllable_boundaries(audio)
        
        # Extract syllable segments
        syllables = self.extract_syllables(audio, boundaries)
        
        # Extract features for each syllable
        for syllable in syllables:
            syllable['features'] = self.extract_features(syllable['audio'])
        
        return syllables
    
    def analyze_file(self, audio_path):
        """Analyze audio file"""
        audio, _ = self.load_audio(audio_path)
        return self.analyze_audio(audio)
    
    def get_syllable_count(self, audio):
        """Get the number of syllables detected in audio"""
        boundaries = self.detect_syllable_boundaries(audio)
        return len(boundaries)


if __name__ == "__main__":
    # Test the analyzer
    analyzer = SyllableAnalyzer()
    print("Syllable Analyzer initialized successfully!")
    print(f"Sample rate: {analyzer.sample_rate} Hz")
    print(f"Syllable duration range: {analyzer.min_syllable_duration}s - {analyzer.max_syllable_duration}s")
