from config import QDRANT_API_KEY, QDRANT_API_URL
from core.scripts.qdrant.base import VectorAsyncReader
from logs.logger import get_logger
from qdrant_client import AsyncQdrantClient

logger = get_logger(__name__)


class QdrantAsyncManager(VectorAsyncReader):
    """
    Manager for reading Qdrant vectors asynchronously.

    Attributes
    ----------
    client: AsyncQdrantClient
        The Qdrant client to use.
    collection_name: str
        The name of the collection to read the vectors from.
    """

    def __init__(self, collection_name: str, url: str = QDRANT_API_URL, api_key: str = QDRANT_API_KEY):
        self.client = AsyncQdrantClient(url=url, api_key=api_key)
        self.collection_name = collection_name

    async def search(self, query_vector: list[float], **filters) -> list[dict]:
        result = await self.client.search(collection_name=self.collection_name, query_vector=query_vector, **filters)
        return [{"id": r.id, "score": r.score, "payload": r.payload} for r in result]
