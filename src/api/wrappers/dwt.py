from wrappers.model import Model
from typing import Any
import pickle
import librosa
import dtcwt
import scipy
import numpy as np
import sklearn
from collections import Counter


# Niley model
class DWT(Model):
    
    def __init__(self, model_path: str):
        super().__init__(model_path)
        
    def load(self, model_path: str):
        with open(model_path, "rb") as file:
            self.model = pickle.load(file)
        
    def extract_feature(song_path:str) -> Any:  
        
        def calculate_entropy(list_values):
            counter_values = Counter(list_values).most_common()
            probabilities = [elem[1]/len(list_values) for elem in counter_values]
            entropy=scipy.stats.entropy(probabilities)
            return entropy

        def calculate_statistics(list_values):
            n5 = np.nanpercentile(list_values, 5)
            n25 = np.nanpercentile(list_values, 25)
            n75 = np.nanpercentile(list_values, 75)
            n95 = np.nanpercentile(list_values, 95)
            median = np.nanpercentile(list_values, 50)
            mean = np.nanmean(list_values)
            std = np.nanstd(list_values)
            var = np.nanvar(list_values)
            rms = np.nanmean(np.sqrt(list_values**2))
            return [n5, n25, n75, n95, median, mean, std, var, rms]

        def calculate_crossings(list_values):
            zero_crossing_indices = np.nonzero(np.diff(np.array(list_values) > 0))[0]
            no_zero_crossings = len(zero_crossing_indices)
            mean_crossing_indices = np.nonzero(np.diff(np.array(list_values) > np.nanmean(list_values)))[0]
            no_mean_crossings = len(mean_crossing_indices)
            return [no_zero_crossings, no_mean_crossings]

        def get_features(list_values):
            entropy = calculate_entropy(list_values)
            crossings = calculate_crossings(list_values)
            statistics = calculate_statistics(list_values)
            return [entropy] + crossings + statistics
          
        d, _ = librosa.load(song_path)

        trans = dtcwt.Transform1d(biort='antonini', qshift='qshift_d')
        
        forw = trans.forward(d, nlevels=17)
        features = []
        for coeff in forw.highpasses:
            temp = (np.abs(coeff.squeeze()))
            features += get_features(temp)
            
        features += get_features(forw.lowpass.squeeze())  
    
        return features

        
    def predict(self, song_path: str) -> str:
        X = DWT.extract_feature(song_path)
        print(X)
        y = self.model.predict([X])
        
        genre =['blues', 'classical', 'country', \
            'disco', 'hiphop', 'jazz', 'metal',  \
            'pop', 'reggae', 'rock']

        return genre[y[0]]