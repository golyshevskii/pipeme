from config import QDRANT_API_KEY, QDRANT_API_URL
from qdrant_client import AsyncQdrantClient, QdrantClient


def get_qdrant_client(async_client: bool = False) -> QdrantClient | AsyncQdrantClient:
    if async_client:
        return AsyncQdrantClient(url=QDRANT_API_URL, api_key=QDRANT_API_KEY)
    return QdrantClient(url=QDRANT_API_URL, api_key=QDRANT_API_KEY)
