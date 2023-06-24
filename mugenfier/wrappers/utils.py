import cv2 
import numpy as np
from pylab import imshow
import librosa
# from essentia import Pool 
import matplotlib.pyplot as plt
# from essentia.standard import FrameGenerator, MonoLoader, \
#     Windowing, Spectrum, MFCC


# def extract_mfcc(src: str, dst: str):
#     # we start by instantiating the audio loader:
#     loader = MonoLoader(filename=src)

#     # and then we actually perform the loading:
#     audio = loader()

#     w = Windowing(type = 'hann')
#     spectrum = Spectrum()  # FFT() would return the complex FFT, here we just want the magnitude spectrum
#     mfcc = MFCC()    

#     pool = Pool()

#     for frame in FrameGenerator(audio, frameSize = 1024, hopSize = 512, startFromZero=True):
#         _, mfcc_coeffs = mfcc(spectrum(w(frame)))
#         pool.add('lowlevel.mfcc', mfcc_coeffs)

#     imshow(pool[f'lowlevel.mfcc'].T[1:,:], aspect='auto', origin='lower', interpolation='none')
#     plt.axis('off')
#     plt.savefig(f'{dst}/mfcc.png', bbox_inches='tight', pad_inches=0)


def get_mfcc(song_path: str):
    x , sr = librosa.load(song_path)

    mfccs = librosa.feature.mfcc(y= x, sr=sr)
    
    img = cv2.imread(mfccs)
    img = cv2.resize(img, (256, 192))
    img = np.array(img, dtype=np.float32)

    return img

if __name__ == '__main__':

    import librosa

    # Load an audio file
    y, sr = librosa.load('./yellow.mp3')

    # Compute MFCC features
    mfcc = librosa.feature.mfcc(y=y, sr=sr)


    plt.figure(figsize=(10, 4))
    librosa.display.specshow(mfcc, x_axis='time', sr=sr)
    plt.colorbar()
    plt.title('MFCC')
    plt.tight_layout()
    plt.show()


    # print(mfccs.shape)


    # mfcc = get_mfcc('./yellow.mp3')
    # print(mfcc)
