from typing import List
from sentence_transformers import SentenceTransformer
from config import settings


class EmbeddingModel:

    def __init__(self, model_name: str = None):

        self.model_name = model_name or settings.EMBEDDING_MODEL
        self.model = SentenceTransformer(self.model_name)

    def embed_text(self, text: str) -> List[float]:
        return self.model.encode(text).tolist()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(texts)
        return [e.tolist() for e in embeddings]