"""
Training system for collecting and managing Hebrew syllable pronunciations
"""
import os
import json
import numpy as np
import soundfile as sf
from datetime import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SYLLABLES_DIR, TRAINING_DATA_DIR, SAMPLE_RATE, TARGET_SYLLABLE_COUNT
from src.hebrew_syllables import get_syllable_list
from src.syllable_analyzer import SyllableAnalyzer


class SyllableTrainingSystem:
    """
    Manages the training process for Hebrew syllables
    Allows users to record correct pronunciations of target syllables
    """
    
    def __init__(self):
        self.syllable_list = get_syllable_list()
        self.analyzer = SyllableAnalyzer()
        
        # Ensure directories exist
        os.makedirs(SYLLABLES_DIR, exist_ok=True)
        os.makedirs(TRAINING_DATA_DIR, exist_ok=True)
        
        # Load or initialize training progress
        self.progress_file = os.path.join(TRAINING_DATA_DIR, 'training_progress.json')
        self.load_progress()
    
    def load_progress(self):
        """Load training progress from file"""
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                self.progress = json.load(f)
        else:
            # Initialize progress for all syllables
            self.progress = {
                syllable: {
                    'trained': False,
                    'recordings': [],
                    'quality_score': 0.0,
                    'feature_vector': None
                }
                for syllable in self.syllable_list
            }
            self.save_progress()
    
    def save_progress(self):
        """Save training progress to file"""
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, ensure_ascii=False, indent=2)
    
    def get_training_status(self):
        """Get overall training status"""
        trained_count = sum(1 for data in self.progress.values() if data['trained'])
        total_count = len(self.syllable_list)
        completion_percentage = (trained_count / total_count) * 100
        
        return {
            'trained': trained_count,
            'total': total_count,
            'percentage': completion_percentage,
            'remaining': total_count - trained_count
        }
    
    def get_next_syllable_to_train(self):
        """Get the next syllable that needs training"""
        for syllable in self.syllable_list:
            if not self.progress[syllable]['trained']:
                return syllable
        return None
    
    def save_syllable_recording(self, syllable, audio_data, label="correct"):
        """
        Save a training recording for a specific syllable
        """
        # Create syllable-specific directory
        syllable_dir = os.path.join(SYLLABLES_DIR, syllable.replace('/', '_'))
        os.makedirs(syllable_dir, exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{label}_{timestamp}.wav"
        filepath = os.path.join(syllable_dir, filename)
        
        # Save audio
        sf.write(filepath, audio_data, SAMPLE_RATE)
        
        # Extract features
        features = self.analyzer.extract_features(audio_data)
        
        # Update progress
        self.progress[syllable]['recordings'].append({
            'filepath': filepath,
            'timestamp': timestamp,
            'label': label,
            'features': features.tolist()
        })
        
        # Calculate average feature vector
        all_features = [rec['features'] for rec in self.progress[syllable]['recordings']]
        avg_features = np.mean(all_features, axis=0)
        self.progress[syllable]['feature_vector'] = avg_features.tolist()
        
        # Mark as trained if we have at least one recording
        self.progress[syllable]['trained'] = True
        self.progress[syllable]['quality_score'] = 1.0  # Can be improved with actual quality assessment
        
        self.save_progress()
        
        return filepath
    
    def get_syllable_reference(self, syllable):
        """
        Get the reference audio and features for a trained syllable
        """
        if syllable not in self.progress or not self.progress[syllable]['trained']:
            return None
        
        data = self.progress[syllable]
        if len(data['recordings']) == 0:
            return None
        
        # Return the most recent recording
        latest_recording = data['recordings'][-1]
        
        return {
            'filepath': latest_recording['filepath'],
            'features': np.array(data['feature_vector']),
            'quality_score': data['quality_score']
        }
    
    def get_all_trained_syllables(self):
        """Get list of all trained syllables"""
        return [syl for syl, data in self.progress.items() if data['trained']]
    
    def reset_training(self, syllable=None):
        """Reset training progress for a specific syllable or all syllables"""
        if syllable:
            if syllable in self.progress:
                self.progress[syllable] = {
                    'trained': False,
                    'recordings': [],
                    'quality_score': 0.0,
                    'feature_vector': None
                }
        else:
            self.load_progress()  # Reinitialize all
        
        self.save_progress()
    
    def export_training_data(self, output_path=None):
        """Export all training data for ML model"""
        if output_path is None:
            output_path = os.path.join(TRAINING_DATA_DIR, 'syllable_features.npz')
        
        syllables = []
        features = []
        labels = []
        
        for syllable, data in self.progress.items():
            if data['trained'] and data['feature_vector']:
                syllables.append(syllable)
                features.append(data['feature_vector'])
                labels.append(syllable)
        
        # Save as numpy arrays
        np.savez(
            output_path,
            syllables=np.array(syllables),
            features=np.array(features),
            labels=np.array(labels)
        )
        
        return output_path


if __name__ == "__main__":
    # Test the training system
    training_system = SyllableTrainingSystem()
    
    status = training_system.get_training_status()
    print(f"Training Status:")
    print(f"  Trained: {status['trained']}/{status['total']}")
    print(f"  Completion: {status['percentage']:.1f}%")
    print(f"  Remaining: {status['remaining']}")
    
    next_syllable = training_system.get_next_syllable_to_train()
    if next_syllable:
        print(f"\nNext syllable to train: {next_syllable}")
