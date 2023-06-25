from scipy.io import wavfile

def load_wav(filename: str):
    wav = wavfile.read(filename)
    wav = wav[1]/2.0**15
    return wav

def get_wav_path(path: str, genre: str, index: int):
    wav_path = f'{path}/{genre}/{genre}.000{index}.wav'
    if index >= 0 and index < 10:
        wav_path = f'{path}/{genre}/{genre}.0000{index}.wav' 
    return wav_path
