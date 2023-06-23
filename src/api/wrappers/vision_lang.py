from wrappers.model import Model
from typing import Any
from keras.models import load_model

from pylab import imshow
from essentia import Pool 
import matplotlib.pyplot as plt
from essentia.standard import FrameGenerator, MonoLoader, \
    Windowing, Spectrum, MFCC

import cv2
import re
import numpy as np
import subprocess


plt.rcParams['figure.figsize'] = (16, 9)


def extract_mfcc(src: str, dst: str):
    # we start by instantiating the audio loader:
    loader = MonoLoader(filename=src)

    # and then we actually perform the loading:
    audio = loader()

    w = Windowing(type = 'hann')
    spectrum = Spectrum()  # FFT() would return the complex FFT, here we just want the magnitude spectrum
    mfcc = MFCC()    

    pool = Pool()

    for frame in FrameGenerator(audio, frameSize = 1024, hopSize = 512, startFromZero=True):
        _, mfcc_coeffs = mfcc(spectrum(w(frame)))
        pool.add('lowlevel.mfcc', mfcc_coeffs)

    imshow(pool[f'lowlevel.mfcc'].T[1:,:], aspect='auto', origin='lower', interpolation='none')
    plt.axis('off')
    plt.savefig(f'{dst}/mfcc.png', bbox_inches='tight', pad_inches=0)


def clean(jsondata : str):
    jsondata = jsondata.replace("{\"text\":", "")
    jsondata = jsondata.replace("}", "")
    jsondata = jsondata.replace("\"", "")

    not_allowed = r"[!@#$%^&*-+=<>/\\|'\"`~]"

    jsondata = re.sub(not_allowed, "" , jsondata)

    for i in range(1,len(jsondata)):
        if jsondata[i].isupper() and jsondata[i-1] != " ":
            jsondata = jsondata[:i] + ". " + jsondata[i:]
            
    return jsondata


def clean_and_get_embedding_all(lyric):
    model = "text-embedding-ada-002"

    lyric = clean(lyric)
            
    lbracket = "{"
    rbracket = "}"
    
    output = subprocess.check_output(f"curl http://localhost:8080/v1/embeddings -H \"Authorization: Bearer OPENAI_API_KEY\" -H \"Content-Type: application/json\" -d \'{lbracket} \"input\": \"{lyric}\", \"model\": \"{model}\" {rbracket}\' " , shell=True)
    result = output.decode()
   
    result = re.findall(r"\[-?\d.*\d\]",result)
    result = [float(x) for x in re.findall(r"-?\d+\.?\d+",result[0])]
    
    return result
            
            
def get_transcription(fullpath):      
        
    model = "whisper-tiny.bin"
    if fullpath.find(".mp3") == -1 and fullpath.find(".wav") == -1:
        return -1

    output = subprocess.check_output(f"curl http://localhost:8080/v1/audio/transcriptions -H \"Content-Type: multipart/form-data\" -F file=\"{fullpath}\" -F model=\"{model}\"", shell = True)
    result = output.decode()
            
    return result


def get_text_embedding(song_path):
    path = f"@$PWD/{song_path}"
    lyric = get_transcription(path)
    print(lyric)
    embedding = clean_and_get_embedding_all(lyric)   
    print(embedding)


# Marcos and David model
class VisionLang(Model):

    def __init__(self, models_path: dict):
        super().__init__(models_path)
        
    def load(self, models_path: dict):
        self.encoder = load_model(models_path['encoder'])
        self.model = load_model(models_path['vision_lang'])

    def extract_feature(self, song_path:str) -> Any:
        
        feature: list = get_text_embedding(song_path)

        extract_mfcc(song_path, '.')

        img = cv2.imread(f'./mfcc.png')
        img = cv2.resize(img, (256, 192))
        img = np.array(img, dtype=np.float32)

        mfcc_embedding = self.encoder.predict(img)

        feature.extend(mfcc_embedding)

        return feature
        
    def predict(self, song_path: str) -> str:
        # missing implementation
        X = self.extract_feature(song_path)
        
        print(self.model.predict(X))
        
        return "classic"


# #the embeddings for gtzan can be downloaded from here: https://drive.google.com/file/d/1YNlG1jlRcwyKRF6iSLce5-He1EodpiDW/view?usp=drive_link            
# if __name__ == '__main__':    
    
#     path = f"@/home/leandro/study/projects/mugenfier/src/api/wrappers/yellow.mp3"
#     lyric = get_transcription(path)
#     print(lyric)
#     embedding = clean_and_get_embedding_all(lyric)   
#     print(embedding)
