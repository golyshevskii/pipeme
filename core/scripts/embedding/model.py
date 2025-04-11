from abc import ABC, abstractmethod

from sentence_transformers import SentenceTransformer


class BaseEmbeddingModel(ABC):
    """Base class for embedding models."""

    @abstractmethod
    def encode(self, data: str | list[str]) -> list[float] | list[list[float]]:
        """
        Encode data using the defined embedding model.

        Params
        ------
        data: The data to encode.
        """
        pass


class EmbeddingModel(BaseEmbeddingModel):
    """
    Embedding model using SentenceTransformer.

    Attributes
    ----------
    model: SentenceTransformer
        The SentenceTransformer model.
    model_name_or_path: str
        The name or path of the model to use.
    """

    def __init__(self, model_name_or_path: str = "jinaai/jina-embeddings-v3"):
        self.model = SentenceTransformer(model_name_or_path, trust_remote_code=True)
        self.model_name_or_path = model_name_or_path

    def encode(self, data: str | list[str]) -> list[float] | list[list[float]]:
        return self.model.encode(data).tolist()
