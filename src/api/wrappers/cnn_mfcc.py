from model import Model
from typing import Any


# Raul model
class CNN_MFCC(Model):
    
    def __init__(self, model_path: str):
        super().__init__(model_path)
        
    def load():
        # missing implementation
        ...
        
    def extract_feature() -> Any:
        # missing implementation
        ...
        
    def predict(song_path: str) -> str:
        # missing implementation
        return "classic"