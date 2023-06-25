
from typing import Any
from numpy import floating, ndarray
import matplotlib.pyplot as plt
import numpy as np
import librosa
import cv2 as cv
from tensorflow import convert_to_tensor
import os


def extract_spec(wav: ndarray[floating[Any]], sr: float, save_img: bool = False, dst: str = '.'):
    features = {}
    
    # Calculate the MFCCs
    features['mfcc'] = librosa.feature.mfcc(y=wav, sr=sr),

    # Calculate the Mel Spectrogram
    features['mel'] = librosa.feature.melspectrogram(y=wav, sr=sr),
        
    # Calculate the Log Mel Spectrogram
    features['log_mel'] = librosa.power_to_db(features['mel'])
    
    plt.figure(figsize=(16, 9))
    plt.axis('off')

    for feat in features:
        # librosa.display.specshow(features[feat][0], x_axis='time')
        plt.imshow(features[feat][0], aspect='auto', origin='lower', interpolation='none')
        plt.savefig(f'{dst}/{feat}.png', bbox_inches='tight', pad_inches=0)

        X = cv.imread(f'{dst}/{feat}.png')
        X = cv.resize(X, (256, 192))
        X = np.array(X, dtype=np.float32)
        X = convert_to_tensor(X)
        
        if not save_img:
            os.remove(f'{dst}/{feat}.png')

        features[feat] = X

    plt.close()
    
    return features
