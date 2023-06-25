import sys
sys.path.append('..')

from mugenfier import GTZAN

GENRES = ['blues', 'classical', 'country', 'disco', \
    'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']

if __name__ == '__main__':
    dataset = GTZAN('../mugenfier/datasets/gtzan')
    
    split = {
        'train': { genre: [i for i in range(80)] for genre in GENRES },
        'val': { genre: [i for i in range(80,90)] for genre in GENRES },
        'test': { genre: [i for i in range(90,100)] for genre in GENRES },
    }
    
    dataset.set_split(split)

    for wav in dataset['pop']['test']:
        print(wav)
 