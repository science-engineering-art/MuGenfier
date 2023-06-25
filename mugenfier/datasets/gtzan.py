import tarfile
from copy import deepcopy
from mugenfier.utils import is_valid_split, load_wav, get_wav_path
import pandas as pd
from mugenfier.features import extract_spec
import numpy as np


SETS = {'test', 'train', 'val'}

GENRES = {'blues', 'classical', 'country', 'disco', \
    'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock'}


class GTZAN:

    def __init__(self, path: str):
        self.path = path
        self.split = dict()
        self.descompress()

    def descompress(self):
        if self.path.endswith('.tar.gz'):
            tar = tarfile.open(self.path, 'r:gz')
            tar.extractall(
                ''.join(self.path.split('/')[:-1])   
            )
            tar.close()

    def set_split(self, split: dict):
        
        if is_valid_split(split):
            self.split = deepcopy(split)
            
    def filter_by_genre(self, genre: str):

        def filter_by_set(set: str):
            for index in self.split[set][genre]:                
                wav_path = get_wav_path(self.path, genre, index)
                if wav_path.endswith('jazz.00054.wav'): 
                    continue
                wav, sr = load_wav(wav_path)
                yield wav, sr
        
        return { set: filter_by_set(set) for set in SETS }

    def filter_by_set(self, set: str):

        def filter_by_genre(genre: str):
            for index in self.split[set][genre]:                
                wav_path = get_wav_path(self.path, genre, index)
                if wav_path.endswith('jazz.00054.wav'): 
                    continue
                wav, sr = load_wav(wav_path)
                yield wav, sr
        
        return { genre: filter_by_genre(genre) for genre in GENRES }

    def get_dataframe(self):
        cache_path = f'{self.path}/cache.h5'
        store = pd.HDFStore(cache_path)
        
        if 'df' in store:
            df = store['df']
            
            one_hot = pd.get_dummies(df['genre'])
            df = pd.concat([df, one_hot], axis=1) 
            df.drop(['genre'], axis=1, inplace=True)
            
            return df        
            
        dataset = []
        
        print('PREPROCESSING...\n')
        for set in SETS:
            for genre in GENRES:
                for wav, sr in self[set][genre]:
                    features = extract_spec(wav, sr)
                    
                    dataset.append([
                        features['mfcc'],
                        features['mel'],
                        features['log_mel'],
                        set,
                        genre
                    ])
                    
                print(f'({set.upper()}, {genre.upper()}): DONE!!\n')
        
        df = pd.DataFrame(
            data=np.array(dataset, dtype=object), 
            columns=['mfcc', 'mel', 'log_mel', 'set', 'genre']
        )
        
        store['df'] = df 
            
        one_hot = pd.get_dummies(df['genre'])
        df = pd.concat([df, one_hot], axis=1)
        df.drop(['genre'], axis=1, inplace=True)
    
        return df

    def __getitem__(self, key: str):
        if key in SETS:
            return self.filter_by_set(key)
        if key in GENRES:
            return self.filter_by_genre(key)
