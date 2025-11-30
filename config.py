"""
Configuration file for Hebrew Speech Correction System
"""
import os

# Project paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
TRAINING_DATA_DIR = os.path.join(DATA_DIR, 'training_data')
SYLLABLES_DIR = os.path.join(DATA_DIR, 'syllables')
RECORDINGS_DIR = os.path.join(DATA_DIR, 'recordings')

# Audio settings
SAMPLE_RATE = 22050  # Hz
CHANNELS = 1  # Mono
CHUNK_SIZE = 1024
AUDIO_FORMAT = 'wav'

# Hebrew syllable settings
TARGET_SYLLABLE_COUNT = 100  # Most common Hebrew syllables to train
MIN_SYLLABLE_DURATION = 0.05  # seconds (more flexible)
MAX_SYLLABLE_DURATION = 1.5  # seconds (allow longer syllables)

# ML Model settings
MODEL_NAME = 'hebrew_syllable_corrector'
EMBEDDING_DIM = 128
SIMILARITY_THRESHOLD = 0.85  # Threshold for pronunciation quality

# Training settings
BATCH_SIZE = 32
LEARNING_RATE = 0.001
EPOCHS = 50

# GUI settings
WINDOW_TITLE = "Hebrew Speech Correction System"
WINDOW_SIZE = "800x600"
THEME_COLOR = "#2E86AB"
