from collections.abc import Iterable
from typing import Any

from config import QDRANT_API_KEY, QDRANT_API_URL
from core.scripts.qdrant.base import VectorReader, VectorWriter
from logs.logger import get_logger
from qdrant_client import QdrantClient
from qdrant_client.http.models import Payload, PointStruct, WriteOrdering

logger = get_logger(__name__)


class QdrantSyncManager(VectorWriter, VectorReader):
    """
    Manager for writing and reading Qdrant vectors.

    Attributes
    ----------
    client: QdrantClient
        The Qdrant client to use.
    collection_name: str
        The name of the collection to sync the vectors to.
    """

    def __init__(self, collection_name: str, url: str = QDRANT_API_URL, api_key: str = QDRANT_API_KEY):
        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection_name = collection_name

    def build_points(self, vectors: list[dict[str, Any]]) -> list[PointStruct]:
        """
        Build a list of PointStruct objects.

        Params
        ------
        vectors: The vectors data to build the points from.

        The data must be a list of dictionaries with the following keys:
            - id (str | int): The id of the vector point.
            - vector (list[float]): The vector to upsert.
            - payload (dict): The payload of the vector. Used to store additional information and metadata.
        """
        points = []
        processed_ids = set()

        logger.debug("Building points from vectors...")
        for vector in vectors:
            vid = vector["id"]
            if vid in processed_ids:
                logger.warning("Vector %s already exists in points. Skipping.", vid)
                continue
            points.append(PointStruct(id=vid, vector=vector["vector"], payload=Payload(**vector["payload"])))
            processed_ids.add(vid)
        logger.debug("Vectors points built. Amount: %s", len(points))
        return points

    def upsert(
        self,
        points: Iterable[dict | PointStruct],
        wait: bool = True,
        ordering: WriteOrdering = WriteOrdering.MEDIUM,
        **kwargs,
    ) -> None:
        if isinstance(points, dict):
            points = self.build_points(points)
        result = self.client.upsert(
            collection_name=self.collection_name, points=points, wait=wait, ordering=ordering, **kwargs
        )
        logger.info(
            "Vectors upsert status: %(status)s. Operation ID: %(id)s",
            {"id": result.operation_id, "status": result.status},
        )
        return result
