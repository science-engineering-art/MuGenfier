from wrappers.cnn_mfcc import CNN_MFCC
from wrappers.dwt import DWT
from wrappers.vision_lang import VisionLang

dwt = DWT("../../models/dwt.bin")
# siam = VisionLang("<path>")
# cnn = CNN_MFCC("<path>")

def predict(model: str, song_path: str) -> str:
    if model == "dwt":
        return dwt.predict(song_path)
    # elif model == "vision_lang":
    #     return siam.predict(song_path)
    # elif model == "cnn_mfcc":
    #     return cnn.predict(song_path)
    else:
        return "Without Genre"
