import pandas as pd
from .gtzan import GENRES
from mugenfier.features import FEATURES
# import numpy as np

def split_dataframe(df: pd.DataFrame):
    
    df_train = df[df['set'].apply(lambda s: s == 'train')]
    df_train = pd.concat([df_train[list(FEATURES)], df_train[list(GENRES)]])
    # df_train.drop(['set'], axis=1, inplace=True)
    
    df_val = df[df['set'].apply(lambda s: s == 'val')]
    df_val = pd.concat([df_val[list(FEATURES)], df_val[list(GENRES)]])
    # df_val.drop(['set'], axis=1, inplace=True)
    
    df_test = df[df['set'].apply(lambda s: s == 'test')]
    df_test = pd.concat([df_test[list(FEATURES)], df_test[list(GENRES)]])
    # df_test = df_test[df_test['mfcc'].apply(lambda s: not s.isna())]
    # df_test.drop(['set'], axis=1, inplace=True)
    
    return df_train, df_val, df_test
    