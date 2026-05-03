from FlagEmbedding import FlagModel
from typing import List

class Embedder:
    def __init__(self, model_name: str = "BAAI/bge-m3"):
        self.model = FlagModel(
            model_name,
            use_fp16=True,
            normalize_embeddings=True
        )
    
    def encode(self, texts: List[str]) -> List[List[float]]:
        """Encode texts into embeddings using BAAI/bge-m3"""
        embeddings = self.model.encode(texts)
        return embeddings.tolist()
    
    def encode_single(self, text: str) -> List[float]:
        """Encode single text into embedding"""
        embedding = self.model.encode([text])
        return embedding[0].tolist()