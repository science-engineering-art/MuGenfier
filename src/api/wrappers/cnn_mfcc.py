from wrappers.model import Model
from typing import Any
import os
import librosa
import numpy as np
from PIL import Image
from keras.models import load_model
from PIL import Image
import numpy as np


# Raul model
class CNN_MFCC(Model):
    
    def __init__(self, model_path: str):
        super().__init__(model_path)
        
    def load(self, model_path: str):
        loaded_model = load_model(model_path)
        return loaded_model
        
    def extract_feature(self, song_path:str) -> Any:
        x , sr = librosa.load(song_path)
        mfccs = librosa.feature.mfcc(y=x, sr=sr)
        img_array = np.array(mfccs)
        img_array = img_array / 255.0  # Normalización de los datos
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
        
    def predict(self, song_path: str) -> str:
        img_array = self.extract_feature(song_path)
        prediction = self.model.predict(img_array)
        genres = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
        genre = genres[np.argmax(prediction)] 

        return { "genre": genre }


if __name__ == "__main__":
    model_path = "src/training/models/model.h5" #agregar modelo preentrenado
    cnn_mfcc = CNN_MFCC(model_path)
    song_path = "audi.wav"
    predicted_genre = cnn_mfcc.predict(song_path)
    print(predicted_genre)

