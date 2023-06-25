from wrappers.cnn_mfcc import CNN_MFCC
from wrappers.dtcwt import DTCWT
from wrappers.vision_lang import VisionLang

dtcwt = DTCWT("../../models/dtcwt.bin")

vis = VisionLang({
    'encoder': '../../models/encoder.keras', 
    'vision_lang': '../../models/vision_lang.keras'
})

cnn = CNN_MFCC("../../models/cnn_mfcc.h5")

def predict(model: str, song_path: str) -> str:
    if model == "dwt":
        return dtcwt.predict(song_path)
    elif model == "vision_lang":
        return vis.predict(song_path)
    elif model == "cnn_mfcc":
        return cnn.predict(song_path)
    else:
        return "Without Genre"
