from dataclasses import dataclass

@dataclass
class TextEmbedding:
    text: str
    embedding: list[float]
