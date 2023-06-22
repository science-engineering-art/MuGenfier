from cnn_mfcc import CNN_MFCC
from dwt import DWT
from siamese import Siamese

dwt = DWT("<path>")
siam = Siamese("<path>")
cnn = CNN_MFCC("<path>")

def predict(model: str, song_path: str) -> str:
    if model == "dwt":
        return dwt.predict(song_path)
    elif model == "siamese":
        return siam.predict(song_path)
    elif model == "cnn_mfcc":
        return cnn.predict(song_path)
    else:
        return "Without Genre"
