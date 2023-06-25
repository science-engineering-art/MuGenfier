import sys
sys.path.append('..')

import mugenfier as mg

GENRES = ['blues', 'classical', 'country', 'disco', \
    'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']

if __name__ == '__main__':
    gtzan_path = '../mugenfier/datasets/gtzan'
    dataset = mg.datasets.GTZAN(gtzan_path)

    split = {
        'train': { genre: [i for i in range(80)] for genre in GENRES },
        'val': { genre: [i for i in range(80,90)] for genre in GENRES },
        'test': { genre: [i for i in range(90,100)] for genre in GENRES },
    }

    dataset.set_split(split)

    df = dataset.get_dataframe()
   
    for tensor in df['mfcc']:
        print(tensor)
    
