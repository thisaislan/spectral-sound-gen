import os
import sys
import numpy as np
import wave
import string

def read_text_files_in_directory(directory):
    """Read and concatenate text content from all files in the given directory."""
    combined_text = ""
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    combined_text += f.read() + "\n"
            except (UnicodeDecodeError, IsADirectoryError):
                print(f"Skipping binary or non-text file: {file_path}")
    return combined_text

def text_to_frequencies(text, sample_rate=44100, duration=5):
    """Convert text characters to frequency components."""
    unique_chars = list(set(text))
    char_to_freq = {char: 200 + i * 20 for i, char in enumerate(unique_chars)}
    
    time = np.linspace(0, duration, sample_rate * duration)
    signal = np.zeros_like(time)
    
    for i, char in enumerate(text):
        if char in char_to_freq:
            signal += np.sin(2 * np.pi * char_to_freq[char] * time)
        if i > 500:  # Limit the number of iterations to avoid excessive length
            break
    
    signal = np.int16(signal / np.max(np.abs(signal)) * 32767)
    return signal

def save_waveform(filename, data, sample_rate=22050):
    """Save generated waveform as a .wav file."""
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(data.tobytes())

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_folder>")
        return
    
    folder_path = sys.argv[1]
    text_data = read_text_files_in_directory(folder_path)
    sound_wave = text_to_frequencies(text_data)
    save_waveform("compressed_data.wav", sound_wave)
    print("Generated sound file: compressed_data.wav")

if __name__ == "__main__":
    main()
