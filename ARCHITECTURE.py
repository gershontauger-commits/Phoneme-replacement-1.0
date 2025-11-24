"""
System architecture visualization and component relationships
"""

SYSTEM_ARCHITECTURE = """
┌────────────────────────────────────────────────────────────────────────────┐
│                   HEBREW SPEECH CORRECTION SYSTEM                          │
│                          System Architecture                               │
└────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────── USER INTERFACE ─────────────────────────────────┐
│                                                                             │
│                          ┌──────────────┐                                  │
│                          │   main.py    │                                  │
│                          │   (GUI App)  │                                  │
│                          └──────┬───────┘                                  │
│                                 │                                           │
│                    ┌────────────┼────────────┐                             │
│                    │                          │                             │
│           ┌────────▼─────────┐      ┌────────▼─────────┐                  │
│           │  Training Mode   │      │ Correction Mode  │                  │
│           │  - Record        │      │  - Record        │                  │
│           │  - Save          │      │  - Analyze       │                  │
│           │  - Progress      │      │  - Correct       │                  │
│           └──────────────────┘      └──────────────────┘                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   │
┌──────────────────────────── CORE MODULES ──────────────────────────────────┐
│                                  │                                          │
│    ┌─────────────────────────────▼────────────────────────────┐            │
│    │           AUDIO RECORDING (audio_recorder.py)            │            │
│    │   • Real-time microphone capture                         │            │
│    │   • Multi-threaded queue processing                      │            │
│    │   • Start/Stop controls                                  │            │
│    │   • WAV file export                                      │            │
│    └─────────────────────────────┬────────────────────────────┘            │
│                                   │                                         │
│    ┌─────────────────────────────▼────────────────────────────┐            │
│    │      SYLLABLE ANALYSIS (syllable_analyzer.py)            │            │
│    │   • Energy envelope calculation                          │            │
│    │   • Onset detection                                      │            │
│    │   • Syllable boundary segmentation                       │            │
│    │   • MFCC feature extraction (29D)                        │            │
│    └─────────────────────────────┬────────────────────────────┘            │
│                                   │                                         │
│              ┌────────────────────┼────────────────────┐                   │
│              │                    │                    │                   │
│    ┌─────────▼─────────┐ ┌───────▼────────┐  ┌───────▼────────┐          │
│    │   SYLLABLE DB     │ │   TRAINING     │  │  PRONUNCIATION │          │
│    │ (hebrew_syllables)│ │    SYSTEM      │  │     MODEL      │          │
│    │                   │ │  (training_    │  │ (pronunciation_│          │
│    │ • 100 syllables   │ │   system.py)   │  │   model.py)    │          │
│    │ • CV patterns     │ │                │  │                │          │
│    │ • Frequencies     │ │ • Save refs    │  │ • Neural net   │          │
│    │                   │ │ • Track prog   │  │ • Embeddings   │          │
│    └───────────────────┘ │ • Export data  │  │ • Assessment   │          │
│                          └────────┬───────┘  └────────┬───────┘          │
│                                   │                    │                   │
│                          ┌────────▼────────────────────▼───────┐          │
│                          │   AUDIO CORRECTOR                   │          │
│                          │   (audio_corrector.py)              │          │
│                          │   • Quality assessment              │          │
│                          │   • Syllable matching               │          │
│                          │   • Time-stretching                 │          │
│                          │   • Audio replacement               │          │
│                          │   • Output generation               │          │
│                          └─────────────────────────────────────┘          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   │
┌──────────────────────────── DATA LAYER ────────────────────────────────────┐
│                                  │                                          │
│    ┌─────────────────────────────▼────────────────────────────┐            │
│    │                    DATA STORAGE                           │            │
│    │                                                           │            │
│    │  data/recordings/          data/syllables/               │            │
│    │  ├── recording_*.wav       ├── syllable_1/               │            │
│    │  └── corrected_*.wav       │   ├── correct_*.wav         │            │
│    │                            │   └── ...                   │            │
│    │  data/training_data/       └── syllable_N/               │            │
│    │  ├── progress.json                                       │            │
│    │  └── features.npz          models/                       │            │
│    │                            └── pronunciation_model.pth   │            │
│    └───────────────────────────────────────────────────────────┘            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌────────────────────────── PROCESSING PIPELINE ─────────────────────────────┐
│                                                                             │
│  TRAINING WORKFLOW:                                                         │
│  ─────────────────                                                          │
│                                                                             │
│  User Speaks → Microphone → AudioRecorder → Save Audio                     │
│                                                    ↓                        │
│                              SyllableAnalyzer ← Load Audio                  │
│                                    ↓                                        │
│                              Extract Features (29D)                         │
│                                    ↓                                        │
│                              TrainingSystem                                 │
│                                    ↓                                        │
│                          Store Reference + Features                         │
│                                    ↓                                        │
│                          Update PronunciationModel                          │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  CORRECTION WORKFLOW:                                                       │
│  ────────────────────                                                       │
│                                                                             │
│  User Speaks → Microphone → AudioRecorder → Audio Buffer                   │
│                                                    ↓                        │
│                              SyllableAnalyzer ← Analyze                     │
│                                    ↓                                        │
│                          Detect Syllable Boundaries                         │
│                                    ↓                                        │
│                          Extract Features for Each                          │
│                                    ↓                                        │
│                          PronunciationModel                                 │
│                                    ↓                                        │
│                          Compare with References                            │
│                                    ↓                                        │
│                          Assess Quality (0-1 score)                         │
│                                    ↓                                        │
│                          AudioCorrector                                     │
│                                    ↓                                        │
│                    Identify Syllables < Threshold                           │
│                                    ↓                                        │
│                    Replace with Reference Audio                             │
│                                    ↓                                        │
│                         Time-Stretch to Match                               │
│                                    ↓                                        │
│                        Generate Corrected Audio                             │
│                                    ↓                                        │
│                    Save/Play Corrected Output                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────── ML MODEL ARCHITECTURE ──────────────────────────────┐
│                                                                             │
│  Input: Audio Features (29 dimensions)                                     │
│    ↓                                                                        │
│  ┌──────────────────────────────────────────┐                              │
│  │  Layer 1: Linear(29 → 256)               │                              │
│  │           + ReLU                         │                              │
│  │           + BatchNorm                    │                              │
│  │           + Dropout(0.3)                 │                              │
│  └──────────────────┬───────────────────────┘                              │
│                     ↓                                                       │
│  ┌──────────────────────────────────────────┐                              │
│  │  Layer 2: Linear(256 → 128)              │                              │
│  │           + ReLU                         │                              │
│  │           + BatchNorm                    │                              │
│  │           + Dropout(0.3)                 │                              │
│  └──────────────────┬───────────────────────┘                              │
│                     ↓                                                       │
│  ┌──────────────────────────────────────────┐                              │
│  │  Layer 3: Linear(128 → 128)              │                              │
│  │           + Tanh                         │                              │
│  └──────────────────┬───────────────────────┘                              │
│                     ↓                                                       │
│  Output: Embedding Vector (128 dimensions)                                 │
│                     ↓                                                       │
│  Comparison: Cosine Similarity                                             │
│  Score: (similarity + 1) / 2 → [0, 1]                                      │
│  Decision: score >= 0.85 → Good | score < 0.85 → Needs Correction          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌────────────────────── FEATURE EXTRACTION ──────────────────────────────────┐
│                                                                             │
│  Audio Signal (time domain)                                                │
│    ↓                                                                        │
│  Short-Time Fourier Transform (STFT)                                       │
│    ↓                                                                        │
│  Mel-frequency scale conversion                                            │
│    ↓                                                                        │
│  ┌────────────────────────────────────────┐                                │
│  │  MFCC Features:                        │                                │
│  │  • 13 coefficients (mean)              │  → 13 dimensions               │
│  │  • 13 coefficients (std dev)           │  → 13 dimensions               │
│  └────────────────────────────────────────┘                                │
│    ↓                                                                        │
│  ┌────────────────────────────────────────┐                                │
│  │  Spectral Features:                    │                                │
│  │  • Spectral Centroid (mean)            │  → 1 dimension                 │
│  │  • Spectral Rolloff (mean)             │  → 1 dimension                 │
│  └────────────────────────────────────────┘                                │
│    ↓                                                                        │
│  ┌────────────────────────────────────────┐                                │
│  │  Temporal Features:                    │                                │
│  │  • Zero Crossing Rate (mean)           │  → 1 dimension                 │
│  └────────────────────────────────────────┘                                │
│    ↓                                                                        │
│  Concatenate → Feature Vector (29D)                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""

if __name__ == "__main__":
    print(SYSTEM_ARCHITECTURE)
