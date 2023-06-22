
from abc import abstractmethod
from typing import Any


class Model:
    
    def __init__(self, model_path: str):
        self.model_path = model_path
    
    @abstractmethod
    def load():
        ...

    @staticmethod
    def extract_feature() -> Any:
        ...

    @abstractmethod
    def predict(song_path: str) -> str:
        ...