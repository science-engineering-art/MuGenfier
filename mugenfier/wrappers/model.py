
from abc import abstractmethod
from typing import Any


class Model:
    
    def __init__(self, model_path: str):
        self.load(model_path)
    
    @abstractmethod
    def load(self, model_path: str):
        ...

    @abstractmethod
    def extract_feature(self, song_path: str) -> Any:
        ...

    @abstractmethod
    def predict(self, song_path: str) -> str:
        ...
