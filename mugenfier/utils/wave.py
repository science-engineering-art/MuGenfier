from scipy.io import wavfile

def load_wav(filename: str):
    wav = wavfile.read(filename)
    wav = wav[1]/2.0**15
    return wav
