from wrappers.model import Model
from typing import Any
import librosa
import numpy as np
from keras.models import load_model
import numpy as np


# Raul model
class CNN_MFCC(Model):

    def __init__(self, model_path: str):
        super().__init__(model_path)
        
    def load(self, model_path: str):
        self.model = load_model(model_path)

    def extract_feature(self, song_path:str) -> Any:
        x , sr = librosa.load(song_path)
        mfccs = librosa.feature.mfcc(y=x, sr=sr)
        img_array = np.array(mfccs)
        img_array = img_array / 255.0  # Normalización de los datos
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
        
    def predict(self, song_path: str) -> str:
        img_array = self.extract_feature(song_path)
        
        print(img_array.shape)
        
        try:
            prediction = self.model.predict(img_array)
        except:
            print('ERROR')

        genres = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
        genre = genres[np.argmax(prediction)] 

        return { "genre": genre }
