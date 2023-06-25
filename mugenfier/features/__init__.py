from .mfcc import extract_spec

FEATURES = {'mfcc', 'mel', 'log_mel'}

__all__ = [
    "extract_spec", "FEATURES"
]
name = "mugenfier.features"