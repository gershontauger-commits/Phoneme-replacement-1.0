"""
Main GUI Application for Hebrew Speech Correction System
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import os
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import WINDOW_TITLE, WINDOW_SIZE, THEME_COLOR, MODELS_DIR, TRAINING_DATA_DIR
from src.audio_recorder import AudioRecorder
from src.syllable_analyzer import SyllableAnalyzer
from src.training_system import SyllableTrainingSystem
from src.pronunciation_model import PronunciationModel
from src.audio_corrector import AudioCorrector
from src.hebrew_syllables import get_syllable_pronunciation


class HebrewSpeechCorrectorGUI:
    """
    Main GUI application with training mode and correction mode
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        
        # Initialize components
        self.recorder = AudioRecorder()
        self.analyzer = SyllableAnalyzer()
        self.training_system = SyllableTrainingSystem()
        self.model = PronunciationModel()
        self.corrector = AudioCorrector(self.model, self.training_system)
        
        # State variables
        self.current_mode = tk.StringVar(value="training")
        self.recording_audio = None
        self.corrected_audio = None
        self.current_training_syllable = None
        
        # Setup GUI
        self.setup_ui()
        
        # Load model if exists
        self.load_model_if_exists()
        
        # Initialize Training Mode as default
        self.setup_initial_mode()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Hebrew Speech Correction System",
            font=("Helvetica", 18, "bold")
        )
        title_label.grid(row=0, column=0, pady=10)
        
        # Mode selection
        mode_frame = ttk.LabelFrame(main_frame, text="Mode Selection", padding="10")
        mode_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Radiobutton(
            mode_frame,
            text="Training Mode (Record correct syllables)",
            variable=self.current_mode,
            value="training",
            command=self.switch_mode
        ).grid(row=0, column=0, padx=5)
        
        ttk.Radiobutton(
            mode_frame,
            text="Correction Mode (Analyze and correct speech)",
            variable=self.current_mode,
            value="correction",
            command=self.switch_mode
        ).grid(row=0, column=1, padx=5)
        
        # Notebook for different modes
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Training mode tab
        self.training_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.training_frame, text="Training Mode")
        self.setup_training_ui()
        
        # Correction mode tab
        self.correction_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.correction_frame, text="Correction Mode")
        self.setup_correction_ui()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.grid(row=3, column=0, sticky=(tk.W, tk.E))
    
    def setup_training_ui(self):
        """Setup training mode interface"""
        # Progress frame
        progress_frame = ttk.LabelFrame(self.training_frame, text="Training Progress", padding="10")
        progress_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=10)
        
        self.progress_label = ttk.Label(progress_frame, text="Loading...")
        self.progress_label.grid(row=0, column=0, pady=5)
        
        self.progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress_bar.grid(row=1, column=0, pady=5)
        
        # Current syllable frame
        syllable_frame = ttk.LabelFrame(self.training_frame, text="Current Syllable to Record", padding="10")
        syllable_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Instruction label
        instruction_label = ttk.Label(
            syllable_frame,
            text="Say this syllable clearly when recording:",
            font=("Helvetica", 10)
        )
        instruction_label.grid(row=0, column=0, pady=(5, 0))
        
        self.current_syllable_label = ttk.Label(
            syllable_frame,
            text="",
            font=("Helvetica", 72, "bold"),
            foreground="#2E86AB"
        )
        self.current_syllable_label.grid(row=1, column=0, pady=20)
        
        # Pronunciation guide label (using tk.Label for color support)
        self.pronunciation_label = tk.Label(
            syllable_frame,
            text="Say: (loading...)",
            font=("Helvetica", 40, "bold"),
            fg="#FF6B35",
            bg="#FFFACD",
            relief=tk.RAISED,
            padx=20,
            pady=10
        )
        self.pronunciation_label.grid(row=2, column=0, pady=(10, 15))
        
        # Recording controls
        controls_frame = ttk.Frame(self.training_frame)
        controls_frame.grid(row=2, column=0, pady=20)
        
        self.train_record_btn = tk.Button(
            controls_frame,
            text="🎤 START RECORDING",
            command=self.start_training_recording,
            font=("Helvetica", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            width=20,
            height=2,
            relief=tk.RAISED,
            bd=3
        )
        self.train_record_btn.grid(row=0, column=0, padx=10)
        
        self.train_stop_btn = tk.Button(
            controls_frame,
            text="⏹ STOP & SAVE",
            command=self.stop_training_recording,
            state=tk.DISABLED,
            font=("Helvetica", 14, "bold"),
            bg="#F44336",
            fg="white",
            width=20,
            height=2,
            relief=tk.RAISED,
            bd=3
        )
        self.train_stop_btn.grid(row=0, column=1, padx=10)
        
        tk.Button(
            controls_frame,
            text="⏭ NEXT SYLLABLE",
            command=self.next_training_syllable,
            font=("Helvetica", 14, "bold"),
            bg="#2196F3",
            fg="white",
            width=20,
            height=2,
            relief=tk.RAISED,
            bd=3
        ).grid(row=0, column=2, padx=10)
        
        # Playback controls frame
        playback_frame = ttk.LabelFrame(self.training_frame, text="Review Recording", padding="10")
        playback_frame.grid(row=3, column=0, pady=10)
        
        tk.Button(
            playback_frame,
            text="▶ PLAY SAVED RECORDING",
            command=self.play_saved_syllable,
            font=("Helvetica", 12, "bold"),
            bg="#9C27B0",
            fg="white",
            width=25,
            height=2,
            relief=tk.RAISED,
            bd=3
        ).grid(row=0, column=0, padx=10)
        
        tk.Button(
            playback_frame,
            text="🔄 RE-RECORD THIS SYLLABLE",
            command=self.rerecord_syllable,
            font=("Helvetica", 12, "bold"),
            bg="#FF9800",
            fg="white",
            width=25,
            height=2,
            relief=tk.RAISED,
            bd=3
        ).grid(row=0, column=1, padx=10)
        
        # Update training progress
        self.update_training_progress()
    
    def setup_correction_ui(self):
        """Setup correction mode interface"""
        # Instructions
        instructions = ttk.Label(
            self.correction_frame,
            text="Record Hebrew speech, and the system will analyze and correct pronunciation",
            wraplength=500
        )
        instructions.grid(row=0, column=0, pady=10)
        
        # Recording controls
        controls_frame = ttk.Frame(self.correction_frame)
        controls_frame.grid(row=1, column=0, pady=20)
        
        self.record_btn = ttk.Button(
            controls_frame,
            text="Start Recording",
            command=self.start_recording,
            width=20
        )
        self.record_btn.grid(row=0, column=0, padx=5)
        
        self.stop_btn = ttk.Button(
            controls_frame,
            text="Stop Recording",
            command=self.stop_recording,
            state=tk.DISABLED,
            width=20
        )
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        self.analyze_btn = ttk.Button(
            controls_frame,
            text="Analyze & Correct",
            command=self.analyze_and_correct,
            state=tk.DISABLED,
            width=20
        )
        self.analyze_btn.grid(row=0, column=2, padx=5)
        
        # Results display
        results_frame = ttk.LabelFrame(self.correction_frame, text="Analysis Results", padding="10")
        results_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.correction_frame.rowconfigure(2, weight=1)
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            width=70,
            height=15
        )
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Playback controls
        playback_frame = ttk.Frame(self.correction_frame)
        playback_frame.grid(row=3, column=0, pady=10)
        
        ttk.Button(
            playback_frame,
            text="Play Original",
            command=self.play_original,
            width=20
        ).grid(row=0, column=0, padx=5)
        
        ttk.Button(
            playback_frame,
            text="Play Corrected",
            command=self.play_corrected,
            width=20
        ).grid(row=0, column=1, padx=5)
        
        ttk.Button(
            playback_frame,
            text="Save Corrected Audio",
            command=self.save_corrected,
            width=20
        ).grid(row=0, column=2, padx=5)
    
    def switch_mode(self):
        """Switch between training and correction modes"""
        mode = self.current_mode.get()
        if mode == "training":
            self.notebook.select(0)
            self.update_training_progress()
        else:
            self.notebook.select(1)
    
    def setup_initial_mode(self):
        """Set up initial mode on startup"""
        self.notebook.select(0)  # Select Training Mode tab
        self.update_training_progress()
    
    def update_training_progress(self):
        """Update training progress display"""
        try:
            status = self.training_system.get_training_status()
            
            self.progress_label.config(
                text=f"Trained: {status['trained']}/{status['total']} syllables ({status['percentage']:.1f}%)"
            )
            self.progress_bar['value'] = status['percentage']
            
            # Get next syllable
            self.current_training_syllable = self.training_system.get_next_syllable_to_train()
            if self.current_training_syllable:
                self.current_syllable_label.config(text=self.current_training_syllable)
                pronunciation = get_syllable_pronunciation(self.current_training_syllable)
                self.pronunciation_label.config(text=f"Pronunciation: {pronunciation}")
                print(f"DEBUG: Set syllable={self.current_training_syllable}, pronunciation={pronunciation}")
            else:
                self.current_syllable_label.config(text="✓ All Complete!")
                self.pronunciation_label.config(text="")
                print("DEBUG: All syllables complete")
                
            # Force UI update
            self.root.update_idletasks()
        except Exception as e:
            print(f"Error updating training progress: {e}")
            self.status_var.set(f"Error: {str(e)}")
    
    def next_training_syllable(self):
        """Move to next syllable in training"""
        try:
            # Get next syllable immediately
            self.current_training_syllable = self.training_system.get_next_syllable_to_train()
            
            if self.current_training_syllable:
                self.current_syllable_label.config(text=self.current_training_syllable, foreground="#2E86AB")
                pronunciation = get_syllable_pronunciation(self.current_training_syllable)
                self.pronunciation_label.config(text=f"Pronunciation: {pronunciation}")
                status = self.training_system.get_training_status()
                self.status_var.set(f"Ready to record syllable {status['trained'] + 1}: {self.current_training_syllable}")
            else:
                self.current_syllable_label.config(text="✓ Complete!", foreground="green")
                self.pronunciation_label.config(text="")
                self.status_var.set("All syllables trained!")
            
            # Update progress
            self.update_training_progress()
            self.root.update_idletasks()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load next syllable: {str(e)}")
            self.status_var.set("Error")
    
    def start_training_recording(self):
        """Start recording for training"""
        if not self.current_training_syllable:
            messagebox.showinfo("Training Complete", "All syllables have been trained!")
            return
        
        try:
            self.recorder.start_recording()
            self.train_record_btn.config(state=tk.DISABLED)
            self.train_stop_btn.config(state=tk.NORMAL)
            # Flash red to indicate recording
            self.current_syllable_label.config(foreground="red")
            self.status_var.set(f"🎤 RECORDING NOW: Say '{self.current_training_syllable}' clearly!")
            self.root.update_idletasks()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start recording: {str(e)}")
            self.status_var.set("Error")
            self.train_record_btn.config(state=tk.NORMAL)
            self.train_stop_btn.config(state=tk.DISABLED)
    
    def stop_training_recording(self):
        """Stop recording and save training data"""
        try:
            self.status_var.set("Stopping recording...")
            self.root.update()  # Force UI update
            
            audio = self.recorder.stop_recording()
            
            if audio is not None and len(audio) > 0:
                self.status_var.set("Processing audio...")
                self.root.update()
                
                # Save the recording in a thread to avoid freezing
                def save_in_thread():
                    try:
                        filepath = self.training_system.save_syllable_recording(
                            self.current_training_syllable,
                            audio
                        )
                        
                        # Update model with new reference
                        features = self.analyzer.extract_features(audio)
                        self.model.add_syllable_reference(self.current_training_syllable, features)
                        
                        # Update UI in main thread with visual feedback
                        self.root.after(0, lambda: self.current_syllable_label.config(foreground="green"))
                        self.root.after(0, lambda: self.status_var.set(f"✓ Saved '{self.current_training_syllable}' successfully!"))
                        self.root.after(0, self.update_training_progress)
                        
                        # Auto-advance to next syllable after 1.5 seconds
                        self.root.after(1500, self.next_training_syllable)
                    except Exception as e:
                        self.root.after(0, lambda: messagebox.showerror(
                            "Error",
                            f"Failed to save recording: {str(e)}"
                        ))
                        self.root.after(0, lambda: self.status_var.set("Error"))
                        self.root.after(0, lambda: self.current_syllable_label.config(foreground="#2E86AB"))
                    finally:
                        self.root.after(0, lambda: self.train_record_btn.config(state=tk.NORMAL))
                        self.root.after(0, lambda: self.train_stop_btn.config(state=tk.DISABLED))
                
                threading.Thread(target=save_in_thread, daemon=True).start()
            else:
                messagebox.showerror("Error", "No audio recorded")
                self.train_record_btn.config(state=tk.NORMAL)
                self.train_stop_btn.config(state=tk.DISABLED)
                self.current_syllable_label.config(foreground="#2E86AB")
                self.status_var.set("Ready")
        except Exception as e:
            messagebox.showerror("Error", f"Recording error: {str(e)}")
            self.train_record_btn.config(state=tk.NORMAL)
            self.train_stop_btn.config(state=tk.DISABLED)
            self.current_syllable_label.config(foreground="#2E86AB")
            self.status_var.set("Ready")
    
    def play_saved_syllable(self):
        """Play the saved recording of current syllable"""
        if not self.current_training_syllable:
            messagebox.showinfo("No Syllable", "No syllable selected")
            return
        
        try:
            import soundfile as sf
            import sounddevice as sd
            
            # Check if syllable has been recorded
            recordings = self.training_system.progress.get(self.current_training_syllable, {}).get('recordings', [])
            if not recordings:
                messagebox.showinfo("Not Recorded", f"Syllable '{self.current_training_syllable}' has not been recorded yet")
                return
            
            # Get the latest recording file
            latest_recording = recordings[-1]
            
            # Load and play audio
            audio, sr = sf.read(latest_recording)
            self.status_var.set(f"▶ Playing: {self.current_training_syllable}")
            sd.play(audio, sr)
            sd.wait()
            self.status_var.set("Ready")
        except Exception as e:
            messagebox.showerror("Playback Error", f"Could not play recording: {str(e)}")
            self.status_var.set("Ready")
    
    def rerecord_syllable(self):
        """Allow re-recording the current syllable"""
        if not self.current_training_syllable:
            messagebox.showinfo("No Syllable", "No syllable selected")
            return
        
        result = messagebox.askyesno(
            "Re-record Syllable",
            f"Are you sure you want to re-record '{self.current_training_syllable}'?\n\n"
            "This will replace the existing recording."
        )
        
        if result:
            self.status_var.set(f"Ready to re-record: {self.current_training_syllable}")
            messagebox.showinfo("Ready", "Click 'START RECORDING' to record the syllable again")
    
    def start_recording(self):
        """Start recording for correction"""
        self.recorder.start_recording()
        self.record_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.analyze_btn.config(state=tk.DISABLED)
        self.status_var.set("Recording...")
    
    def stop_recording(self):
        """Stop recording"""
        self.recording_audio = self.recorder.stop_recording()
        
        if self.recording_audio is not None:
            # Save recording
            self.recorder.save_recording(self.recording_audio)
            
            self.record_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.analyze_btn.config(state=tk.NORMAL)
            self.status_var.set("Recording complete. Click 'Analyze & Correct'")
        else:
            messagebox.showerror("Error", "No audio recorded")
            self.record_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.status_var.set("Ready")
    
    def analyze_and_correct(self):
        """Analyze and correct recorded audio"""
        if self.recording_audio is None:
            messagebox.showerror("Error", "No audio to analyze")
            return
        
        # Check if model is trained
        if len(self.model.syllable_references) == 0:
            messagebox.showwarning(
                "Training Required",
                "Please train some syllables first in Training Mode!"
            )
            return
        
        self.status_var.set("Analyzing and correcting...")
        self.results_text.delete(1.0, tk.END)
        
        # Run analysis in background thread
        def analyze_thread():
            try:
                corrected, report = self.corrector.correct_audio(self.recording_audio)
                self.corrected_audio = corrected
                
                # Display results
                self.root.after(0, lambda: self.display_results(report))
                self.root.after(0, lambda: self.status_var.set("Analysis complete"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Analysis failed: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("Error during analysis"))
        
        threading.Thread(target=analyze_thread, daemon=True).start()
    
    def display_results(self, report):
        """Display analysis results with visual syllable breakdown"""
        self.results_text.delete(1.0, tk.END)
        
        results = f"╔═══════════════════════════════════════════════════╗\n"
        results += f"║         HEBREW SPEECH ANALYSIS RESULTS           ║\n"
        results += f"╚═══════════════════════════════════════════════════╝\n\n"
        
        results += f"📊 Summary:\n"
        results += f"   • Total syllables detected: {report['total_syllables']}\n"
        results += f"   • Syllables corrected: {report['syllables_corrected']}\n"
        results += f"   • Average quality: {report['average_quality_before']:.1f}%\n\n"
        
        # Visual syllable timeline
        results += f"🎵 SYLLABLE BREAKDOWN (Timeline):\n"
        results += f"{'─' * 50}\n"
        
        # Group syllables into words (consecutive syllables with <0.2s gap)
        words = []
        current_word = []
        for i, syl in enumerate(report['syllables_analyzed']):
            if i > 0:
                gap = syl['start_time'] - report['syllables_analyzed'][i-1]['end_time']
                if gap > 0.2:  # New word if gap > 0.2 seconds
                    if current_word:
                        words.append(current_word)
                    current_word = []
            current_word.append(syl)
        if current_word:
            words.append(current_word)
        
        # Display words with syllables
        for word_idx, word in enumerate(words, 1):
            word_start = word[0]['start_time']
            word_end = word[-1]['end_time']
            results += f"\n📍 Word #{word_idx} [{word_start:.2f}s - {word_end:.2f}s]:\n"
            
            # Build visual representation
            syllables_str = " | ".join([s['matched_syllable'] for s in word])
            results += f"   Syllables: [ {syllables_str} ]\n"
            
            # Quality indicators
            quality_str = ""
            for syl in word:
                q = syl['quality_score']
                if q >= 0.85:
                    quality_str += "✓ "
                elif q >= 0.70:
                    quality_str += "○ "
                else:
                    quality_str += "✗ "
            results += f"   Quality:   [ {quality_str}]\n"
            
            # Show individual syllable details
            for i, syl in enumerate(word, 1):
                status_icon = "✓" if syl['quality_score'] >= 0.85 else "⚠" if syl['quality_score'] >= 0.70 else "✗"
                results += f"      {i}. {status_icon} '{syl['matched_syllable']}' - Quality: {syl['quality_score']:.0%}\n"
        
        # Corrections summary
        results += f"\n{'─' * 50}\n"
        if report['syllables_corrected'] > 0:
            results += f"\n🔧 CORRECTIONS APPLIED:\n"
            for correction in report['corrections']:
                results += f"   ✗ → ✓  '{correction['syllable']}' at {correction['start_time']:.2f}s\n"
                results += f"          Quality improved: {correction['original_quality']:.0%} → 100%\n"
        else:
            results += f"\n🎉 EXCELLENT! No corrections needed!\n"
        
        results += f"\n{'═' * 50}\n"
        
        self.results_text.insert(1.0, results)
    
    def play_original(self):
        """Play original recording"""
        if self.recording_audio is None:
            messagebox.showinfo("Info", "No recording to play")
            return
        
        threading.Thread(
            target=lambda: self.corrector.play_audio(self.recording_audio),
            daemon=True
        ).start()
    
    def play_corrected(self):
        """Play corrected audio"""
        if self.corrected_audio is None:
            messagebox.showinfo("Info", "No corrected audio available")
            return
        
        threading.Thread(
            target=lambda: self.corrector.play_audio(self.corrected_audio),
            daemon=True
        ).start()
    
    def save_corrected(self):
        """Save corrected audio"""
        if self.corrected_audio is None:
            messagebox.showinfo("Info", "No corrected audio to save")
            return
        
        filepath = self.corrector.save_corrected_audio(self.corrected_audio)
        messagebox.showinfo("Success", f"Corrected audio saved to:\n{filepath}")
    
    def load_model_if_exists(self):
        """Load existing model if available"""
        model_path = os.path.join(MODELS_DIR, 'pronunciation_model.pth')
        if os.path.exists(model_path):
            try:
                self.model.load_model(model_path)
                self.status_var.set(f"Model loaded ({len(self.model.syllable_references)} syllables)")
            except Exception as e:
                print(f"Could not load model: {e}")
        
        # Load trained syllables into model
        trained_syllables = self.training_system.get_all_trained_syllables()
        for syllable in trained_syllables:
            ref_data = self.training_system.get_syllable_reference(syllable)
            if ref_data:
                self.model.add_syllable_reference(syllable, ref_data['features'])
    
    def on_closing(self):
        """Handle application closing"""
        if self.recorder.is_recording():
            self.recorder.stop_recording()
        
        # Save model
        if len(self.model.syllable_references) > 0:
            self.model.save_model()
        
        self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = HebrewSpeechCorrectorGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
