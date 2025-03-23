from typing import Union

from logs.logger import get_logger
from sentence_transformers import SentenceTransformer

logger = get_logger(__name__)


class EmbeddingManager:
    def __init__(self, model_name_or_path: str = "jinaai/jina-embeddings-v3"):
        self.model_name_or_path = model_name_or_path
        self.model = SentenceTransformer(model_name_or_path, trust_remote_code=True)

    def vectorize(self, data: Union[str, list[str]]) -> Union[list[float], list[list[float]]]:
        """
        Vectorize data using the defined embedding model.

        Params
        ------
        data: The data to vectorize.
        """
        logger.debug(f"Vectorizing data using {self.model_name_or_path}...")
        return self.model.encode(data).tolist()
