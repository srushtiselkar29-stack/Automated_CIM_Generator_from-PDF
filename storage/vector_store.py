import numpy as np
from typing import List


class VectorStore:
    """
    Simple in-memory vector store for semantic retrieval
    """

    def __init__(self):

        self.embeddings = []
        self.documents = []

    def add_documents(self, docs: List[str], vectors: List[List[float]]):

        for doc, vec in zip(docs, vectors):
            self.documents.append(doc)
            self.embeddings.append(np.array(vec))

    def search(self, query_vector: List[float], top_k: int = 5):

        query_vec = np.array(query_vector)

        scores = []

        for emb in self.embeddings:

            similarity = np.dot(query_vec, emb) / (
                np.linalg.norm(query_vec) * np.linalg.norm(emb)
            )

            scores.append(similarity)

        top_indices = np.argsort(scores)[-top_k:][::-1]

        results = []

        for idx in top_indices:
            results.append(self.documents[idx])

        return results