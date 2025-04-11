import asyncio

from core.scripts.embedding.model import BaseEmbeddingModel, EmbeddingModel
from logs.logger import get_logger

logger = get_logger(__name__)


class EmbeddingManager:
    """
    Manager for embedding models.

    Attributes
    ----------
    model: BaseEmbeddingModel
        The embedding model to use.
    """

    def __init__(self, model: BaseEmbeddingModel):
        self.model = model

    async def vectorize(self, data: str | list[str]) -> list[float] | list[list[float]]:
        """
        Vectorize data using the embedding model.

        Params
        ------
        data: The data to vectorize.
        """
        model_info = getattr(self.model, "model_name_or_path", "Unknown model")
        logger.debug("Vectorizing data using %s", model_info)
        return await asyncio.to_thread(self.model.encode, data)


EMBEDDING_MANAGER = EmbeddingManager(EmbeddingModel())
