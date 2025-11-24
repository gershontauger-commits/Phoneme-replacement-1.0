"""
Quick test to verify GUI displays pronunciation
"""
import tkinter as tk
from src.hebrew_syllables import COMMON_HEBREW_SYLLABLES, get_syllable_pronunciation

def test_gui():
    root = tk.Tk()
    root.title("Test Pronunciation Display")
    root.geometry("600x400")
    
    # Test syllable
    test_syllable = COMMON_HEBREW_SYLLABLES[0]
    test_pronunciation = get_syllable_pronunciation(test_syllable)
    
    # Hebrew syllable label
    hebrew_label = tk.Label(
        root,
        text=test_syllable,
        font=("Helvetica", 72, "bold"),
        fg="#2E86AB"
    )
    hebrew_label.pack(pady=20)
    
    # Pronunciation label
    pronunciation_label = tk.Label(
        root,
        text=f"Pronunciation: {test_pronunciation}",
        font=("Helvetica", 36, "bold"),
        fg="#FF6B35"
    )
    pronunciation_label.pack(pady=20)
    
    # Info label
    info_label = tk.Label(
        root,
        text="If you see both Hebrew and English pronunciation above, the GUI works!",
        font=("Helvetica", 12)
    )
    info_label.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    test_gui()
