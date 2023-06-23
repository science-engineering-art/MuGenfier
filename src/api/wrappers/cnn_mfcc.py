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
        model_path = os.path.join(, f"{model_name}.h5")
        loaded_model = load_model(model_path)
        return loaded_model
        # missing implementation

    def extract_feature(song_path:str) -> Any:
        # missing implementation
        x , sr = librosa.load(audio_path)
        mfccs = librosa.feature.mfcc(y=x, sr=sr)
        img_array = np.array(mfccs)
        img_array = img_array / 255.0  # Normalización de los datos
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
        
    def predict(song_path: str) -> str:
        # missing implementation
        prediction = loaded_model.predict(img_array)
        genres = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
        genre = genres[np.argmax(prediction)] 

        return { "genre": genre }
