from abc import ABC, abstractmethod
from sentence_transformers import SentenceTransformer

class Model(ABC):
    @abstractmethod
    def determine_similarity(self, left: str | list[str], right: str | list[str]) -> list[list[float]]:
        """ Returns array of scores matches between left and right sentences"""
        pass

class ST(Model):
    def __init__(self, *args, **kwargs):
        self.inner = SentenceTransformer(*args, **kwargs)

    @property
    def max_seq_length(self) -> int:
        return self.inner.max_seq_length

    def determine_similarity(self, left: str | list[str], right: str | list[str]) -> list[list[float]]:
        if isinstance(left, str):
            left = [left]
        if isinstance(right, str):
            right = [right]

        embeddings_left = self.inner.encode(left)
        embeddings_right = self.inner.encode(right)
        tensor = self.inner.similarity(embeddings_left, embeddings_right)
        return [
            [round(float(score), 2) for score in tensor[left_idx]]
            for left_idx, _ in enumerate(left)
        ]

def instance(*args, **kwargs) -> Model:
    return ST(*args, **kwargs)
