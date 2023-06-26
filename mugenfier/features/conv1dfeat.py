import os
import librosa
import numpy as np

def load_audio_file(file_path):
    input_length = 660000  # This is 15 seconds with 44100 sample rate
    data = librosa.core.load(file_path, sr=22050)[0]  # We use librosa to load audio file with sample rate 22050
    if len(data) > input_length:
        data = data[:input_length]
    else:
        data = np.pad(data, (0, max(0, input_length - len(data))), "constant")
    return data

def load_dataset(path):
    genres = os.listdir(path)
    X, y = [], []
    for genre in genres:
        genre_path = os.path.join(path, genre)
        for file_name in os.listdir(genre_path):
            file_path = os.path.join(genre_path, file_name)
            data = load_audio_file(file_path)
            X.append(data)
            y.append(genre)
    return np.array(X), np.array(y)

def extract_features(file_path):
    return load_audio_file(file_path)

if __name__ == "__main__":
    file_path = "path"
    features = extract_features(file_path)
    print(features)
