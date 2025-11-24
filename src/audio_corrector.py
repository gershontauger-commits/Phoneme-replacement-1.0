"""
Audio correction engine for replacing mispronounced syllables
"""
import numpy as np
import librosa
import soundfile as sf
from pydub import AudioSegment
from pydub.playback import play
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SAMPLE_RATE, RECORDINGS_DIR
from src.syllable_analyzer import SyllableAnalyzer
from src.pronunciation_model import PronunciationModel


class AudioCorrector:
    """
    Corrects audio by replacing mispronounced syllables with correct ones
    """
    
    def __init__(self, pronunciation_model, training_system):
        self.model = pronunciation_model
        self.training_system = training_system
        self.analyzer = SyllableAnalyzer()
        self.sample_rate = SAMPLE_RATE
    
    def analyze_and_assess(self, audio):
        """
        Analyze audio and assess each syllable
        Returns list of syllables with assessment
        """
        # Extract syllables
        syllables = self.analyzer.analyze_audio(audio)
        
        # For each syllable, find best matching reference
        assessed_syllables = []
        
        for i, syllable in enumerate(syllables):
            features = syllable['features']
            
            # Find best matching reference syllable
            best_match = None
            best_score = 0.0
            
            for ref_syllable in self.model.syllable_references.keys():
                ref_features = self.model.syllable_references[ref_syllable]['features']
                score = self.model.compare_syllables(features, ref_features)
                
                if score > best_score:
                    best_score = score
                    best_match = ref_syllable
            
            # Assess pronunciation quality
            if best_match:
                assessment = self.model.assess_pronunciation(features, best_match)
            else:
                assessment = {
                    'quality_score': 0.0,
                    'needs_correction': True,
                    'message': 'No reference syllable found'
                }
            
            assessed_syllables.append({
                'index': i,
                'audio': syllable['audio'],
                'start_time': syllable['start_time'],
                'end_time': syllable['end_time'],
                'features': features,
                'matched_syllable': best_match,
                'quality_score': assessment['quality_score'],
                'needs_correction': assessment['needs_correction'],
                'message': assessment['message']
            })
        
        return assessed_syllables
    
    def get_replacement_audio(self, syllable_name):
        """
        Get the reference audio for a syllable to use as replacement
        """
        ref_data = self.training_system.get_syllable_reference(syllable_name)
        
        if ref_data is None:
            return None
        
        # Load the reference audio file
        audio, _ = librosa.load(ref_data['filepath'], sr=self.sample_rate)
        return audio
    
    def replace_syllable(self, original_audio, syllable_info, replacement_audio):
        """
        Replace a syllable in the original audio with replacement audio
        """
        start_sample = int(syllable_info['start_time'] * self.sample_rate)
        end_sample = int(syllable_info['end_time'] * self.sample_rate)
        
        # Time-stretch replacement audio to match original duration
        original_duration = syllable_info['end_time'] - syllable_info['start_time']
        replacement_duration = len(replacement_audio) / self.sample_rate
        stretch_factor = replacement_duration / original_duration
        
        if stretch_factor != 1.0:
            replacement_audio = librosa.effects.time_stretch(replacement_audio, rate=stretch_factor)
        
        # Ensure replacement audio matches the segment length
        segment_length = end_sample - start_sample
        if len(replacement_audio) > segment_length:
            replacement_audio = replacement_audio[:segment_length]
        elif len(replacement_audio) < segment_length:
            # Pad with zeros
            replacement_audio = np.pad(replacement_audio, (0, segment_length - len(replacement_audio)))
        
        # Create new audio with replacement
        corrected_audio = original_audio.copy()
        corrected_audio[start_sample:end_sample] = replacement_audio
        
        return corrected_audio
    
    def correct_audio(self, audio, min_quality_threshold=None):
        """
        Correct all mispronounced syllables in the audio
        Returns corrected audio and correction report
        """
        if min_quality_threshold is None:
            from config import SIMILARITY_THRESHOLD
            min_quality_threshold = SIMILARITY_THRESHOLD
        
        # Analyze and assess all syllables
        assessed_syllables = self.analyze_and_assess(audio)
        
        # Identify syllables that need correction
        syllables_to_correct = [
            s for s in assessed_syllables 
            if s['needs_correction'] and s['matched_syllable']
        ]
        
        corrected_audio = audio.copy()
        corrections_made = []
        
        # Replace each problematic syllable
        for syllable in syllables_to_correct:
            replacement_audio = self.get_replacement_audio(syllable['matched_syllable'])
            
            if replacement_audio is not None:
                corrected_audio = self.replace_syllable(
                    corrected_audio,
                    syllable,
                    replacement_audio
                )
                
                corrections_made.append({
                    'index': syllable['index'],
                    'syllable': syllable['matched_syllable'],
                    'original_quality': syllable['quality_score'],
                    'start_time': syllable['start_time'],
                    'end_time': syllable['end_time']
                })
        
        # Generate report
        report = {
            'total_syllables': len(assessed_syllables),
            'syllables_corrected': len(corrections_made),
            'corrections': corrections_made,
            'average_quality_before': np.mean([s['quality_score'] for s in assessed_syllables]),
            'syllables_analyzed': assessed_syllables
        }
        
        return corrected_audio, report
    
    def save_corrected_audio(self, audio, filename=None):
        """Save corrected audio to file"""
        if filename is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"corrected_{timestamp}.wav"
        
        filepath = os.path.join(RECORDINGS_DIR, filename)
        sf.write(filepath, audio, self.sample_rate)
        print(f"Corrected audio saved to: {filepath}")
        return filepath
    
    def play_audio(self, audio):
        """Play audio using pydub"""
        # Convert numpy array to pydub AudioSegment
        audio_int16 = (audio * 32767).astype(np.int16)
        audio_segment = AudioSegment(
            audio_int16.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=2,
            channels=1
        )
        play(audio_segment)


if __name__ == "__main__":
    print("Audio Corrector module loaded successfully!")
    print("Ready to correct mispronounced Hebrew syllables.")
