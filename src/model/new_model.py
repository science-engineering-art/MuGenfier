import json
import os
import cv2
import random
import shutil
import zipfile
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.models import Model
from pandas import DataFrame
from keras import Sequential
# from sklearn.model_selection import train_test_split, KFold
from keras.layers import Conv2D, UpSampling2D, MaxPooling2D, Input, Cropping2D, Cropping3D, Flatten, Dense, Reshape

SEED_VALUE = 42

SETS = ['training', 'validation', 'tests']
GENRES = ['blues', 'classical', 'country', 'disco', \
    'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']


encoder = tf.keras.saving.load_model(f'storage/encoder_model.keras')

# Fix seed to make training deterministic.
random.seed(SEED_VALUE)
np.random.seed(SEED_VALUE)
tf.random.set_seed(SEED_VALUE)


feature = 'mfcc'
for set in SETS:

    try:
        os.mkdir(f"./dataset/split/{set}/features/mfcc_embedding")
    except:
        pass

    src = f'./dataset/split/{set}/features/'
    for genre in os.listdir(f'{src}/{feature}'):
        
        try:
            os.mkdir(f"./dataset/split/{set}/features/mfcc_embedding/{genre}")
        except:
            pass
        
        for name in os.listdir(f'{src}/{feature}/{genre}'):
            dataset = []
            img = cv2.imread(f'{src}/{feature}/{genre}/{name}')
            img = cv2.resize(img, (256, 192))
            img = np.array(img, dtype=np.float32)
            dataset.append([img, genre])

            df = DataFrame(data=np.array(dataset, dtype=object), columns=[feature, 'genre'])

            one_hot = pd.get_dummies(df['genre'])

            df = pd.concat([df, one_hot], axis=1)
            df.drop(['genre'], axis=1, inplace=True)


            nparr = np.array([tf.convert_to_tensor(img2) for img2 in df[feature]])
            
            
            nparr = nparr / 255
            
            with open(f'./dataset/split/{set}/features/mfcc_embedding/{genre}' + f"/{os.path.splitext(name)[0]}.json", "x") as f:
                json.dump([float(x) for x in encoder(nparr[:1])[0]], f)


