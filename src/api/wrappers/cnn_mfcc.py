from wrappers.model import Model
from typing import Any


# Raul model
class CNN_MFCC(Model):
    
    def __init__(self, model_path: str):
        super().__init__(model_path)
        
    def load(self, model_path: str):
        # missing implementation
        ...
        
    def extract_feature(song_path:str) -> Any:
        # missing implementation
        ...
        
    def predict(song_path: str) -> str:
        # missing implementation
        return "classic"