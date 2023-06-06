import json
import os
import random
import shutil
import zipfile
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
from pandas import DataFrame
# from sklearn.model_selection import train_test_split, KFold
from keras import Sequential
import tensorflow as tf
from tensorflow.keras.models import Model
from keras.layers import Conv2D, UpSampling2D, MaxPooling2D, Input, Cropping2D, Cropping3D, Flatten, Dense, Reshape

SEED_VALUE = 42

SETS = ['training', 'validation', 'tests']
GENRES = ['blues', 'classical', 'country', 'disco', \
    'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']


# encoder = tf.keras.saving.load_model(f'storage/encoder_model.keras')

# Fix seed to make training deterministic.

def create_mfcc_embedding():
    
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
                
                if f"{os.path.splitext(name)[0]}.json" in os.listdir(f'./dataset/split/{set}/features/mfcc_embedding/{genre}'):
                    continue
                
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

def load_data(src: str, 
              random_state: float = SEED_VALUE, shuffle: bool = True, 
              stratify: list = None):
    
    feature1, feature2 = 'lyrics_embedding', 'mfcc_embedding'
    dataset = []
    for genre in os.listdir(f'{src}/{feature1}'):
        for name in os.listdir(f'{src}/{feature1}/{genre}'):
            
            data = []
            
            with open(f'{src}/{feature1}/{genre}/{name}', "r") as f:
                jd = json.load(f)
                data.extend(jd)
                
            name = name.replace("_ebdd","")    
            
            with open(f'{src}/{feature2}/{genre}/{name}', "r") as f:
                jd = json.load(f)
                data.extend(jd)
            
            dataset.append([data, genre])

    df = DataFrame(data=np.array(dataset, dtype=object), columns=['ebdd', 'genre'])

    one_hot = pd.get_dummies(df['genre'])

    df = pd.concat([df, one_hot], axis=1)
    df.drop(['genre'], axis=1, inplace=True)

    return (np.array([tf.convert_to_tensor(data) for img in df['ebdd']]), df[GENRES])


# create_mfcc_embedding()

X_train, Y_train = load_data('./dataset/split/training/features', GENRES)
X_test, Y_test = load_data('./dataset/split/tests/features', GENRES)
X_val, Y_val = load_data('./dataset/split/validation/features', GENRES)




