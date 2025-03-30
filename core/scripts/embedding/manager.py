import asyncio
from typing import Union

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

    async def vectorize(self, data: Union[str, list[str]]) -> Union[list[float], list[list[float]]]:
        model_info = getattr(self.model, "model_name_or_path", "custom model")
        logger.debug("Vectorizing data using %s", model_info)
        return await asyncio.to_thread(self.model.encode, data)


EMBEDDING_MANAGER = EmbeddingManager(EmbeddingModel())
