from config import QDRANT_API_KEY, QDRANT_HOST, QDRANT_PORT
from logs.logger import get_logger
from qdrant_client import AsyncQdrantClient, QdrantClient

logger = get_logger(__name__)

AQDRANT_CLIENT = AsyncQdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY)
QDRANT_CLIENT = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY)
