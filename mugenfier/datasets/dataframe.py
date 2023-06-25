from .gtzan import GTZAN, SETS, GENRES
import pandas as pd
from mugenfier.features import extract_spec
import numpy as np

def get_dataframe(gtzan: GTZAN = None):
    cache_path = f'{gtzan.path}/cache.h5'
    store = pd.HDFStore(cache_path)
    
    if 'df' in store:
        return store['df'] 
    
    dataset = []
    
    for set in SETS:
        for genre in GENRES:
            amount = 0
            for wav, sr in gtzan[set][genre]:
                features = extract_spec(wav, sr)
                print(f'{set.upper()} - {genre.upper()} => {amount}')
                dataset.append([
                    features['mfcc'],
                    features['mel'],
                    features['log_mel'],
                    set,
                    genre
                ])
                amount += 1
    
    df = pd.DataFrame(
        data=np.array(dataset, dtype=object), 
        columns=['mfcc', 'mel', 'log_mel', 'set', 'genre']
    )
    
    one_hot = pd.get_dummies(df['genre'])
    df = pd.concat([df, one_hot], axis=1)
    df.drop(['genre'], axis=1, inplace=True)
   
    store['df'] = df 

    return df
