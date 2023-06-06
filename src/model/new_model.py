import json
from multiprocessing.dummy import active_children
import os
from pickletools import optimize
import random
import shutil
import zipfile
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
from pandas import DataFrame
# from sklearn.model_selection import train_test_split, KFold
import keras as kr
from keras import Sequential
import tensorflow as tf
from tensorflow.keras.models import Model
from keras.layers import Conv2D, UpSampling2D, MaxPooling2D, Input, Cropping2D, Cropping3D, Flatten, Dense, Reshape

SEED_VALUE = 42

SETS = ['training', 'validation', 'tests']
GENRES = ['blues', 'classical', 'country', 'disco', \
    'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']


encoder = tf.keras.saving.load_model(f'storage/encoder_model.keras')

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


nn = [386 + 500, 512, 256, 10]

model = Sequential()
model.add(Dense(nn[1], activation='relu'))
model.add(Dense(nn[2], activation='relu'))
model.add(Dense(nn[3], activation='softmax'))

# model.compile(loss = 'mse', optimizer = kr.optimizer.SGD(lr = 0.05), metrics = ['acc'])
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


history = []

model_storage = './ebddmodel'
try:
    os.mkdir(model_storage)
except:
    pass

if 'model_storage' not in os.listdir(model_storage):
    os.mkdir(f'{model_storage}/model_storage')

last_iter = 0

if len(os.listdir(f'{model_storage}/model_storage')) > 0:
    last_iter = sorted([int(model.removeprefix('model_').removesuffix('.keras'))
        for model in os.listdir(f'{model_storage}/model_storage')], reverse=True)[0]
    model = tf.keras.saving.load_model(f'{model_storage}/model_storage/model_{last_iter}.keras')

for i in range(last_iter, 50):
    history.append(model.fit(x=X_train, y=Y_train, epochs=10, validation_data=(X_val, Y_val)))
    model.save(f'{model_storage}/model_storage/model_{i}.keras')
    
    
# print(model.summary())