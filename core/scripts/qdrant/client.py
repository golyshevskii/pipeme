from config import QDRANT_API_KEY, QDRANT_API_URL
from qdrant_client import AsyncQdrantClient, QdrantClient

AQDRANT_CLIENT = AsyncQdrantClient(url=QDRANT_API_URL, api_key=QDRANT_API_KEY)
QDRANT_CLIENT = QdrantClient(url=QDRANT_API_URL, api_key=QDRANT_API_KEY)
