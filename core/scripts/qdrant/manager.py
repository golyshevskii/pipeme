from config import QDRANT_API_KEY, QDRANT_HOST, QDRANT_PORT
from logs.logger import get_logger
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

logger = get_logger(__name__)

QDRANT = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY)


def upsert_points(
    collection_name: str, points: list[PointStruct], wait: bool = True, client: QdrantClient = QDRANT
) -> dict:
    """
    Upsert points into a collection.

    Params
    ------
        collection_name: The name of the collection to upsert points into.
        points: The points to upsert.
        wait: Whether to wait for the operation to complete.
    """
    result = client.upsert(collection_name=collection_name, points=points, wait=wait)
    logger.debug(f"Upserted {len(points)} vectors into collection {collection_name}")
    return result


def recreate_collection(collection_name: str, client: QdrantClient = QDRANT) -> None:
    """
    Recreate a collection.

    Params
    ------
        collection_name: The name of the collection to create.
    """
    client.recreate_collection(collection_name=collection_name)
    logger.debug(f"Collection {collection_name} created successfully")
