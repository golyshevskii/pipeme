from collections.abc import Iterable
from typing import Any

from config import QDRANT_API_KEY, QDRANT_API_URL
from core.scripts.qdrant.base import VectorWriter
from logs.logger import get_logger
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, Payload, PointStruct, UpdateResult, VectorParams, WriteOrdering

logger = get_logger(__name__)


class QdrantSyncManager(VectorWriter):
    """
    Sync manager for working with Qdrant vectors.

    Attributes
    ----------
    client: Sync QdrantClient
        The Qdrant client to use.
    collection_name: str | None
        The name of the collection to sync the vectors to.
        We can work with one collection (if provided)
        or multiple collections when using methods that require collection name.
    _default_vector_config: VectorParams
        The default vector configuration to use for the collection.
    """

    def __init__(self, collection_name: str | None = None, url: str = QDRANT_API_URL, api_key: str = QDRANT_API_KEY):
        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection_name = collection_name
        self._default_vector_config = VectorParams(size=1024, distance=Distance.COSINE)

    def create_collection(
        self, collection_name: str, vector_config: VectorParams | None = None, **kwargs
    ) -> bool | None:
        """
        Create a specific collection.

        Params
        ------
        collection_name: The name of the collection to create.
        vector_config: The vector configuration to use for the collection.

        Returns
        -------
        True if the collection was created.
        """
        if not self.client.collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name, vectors_config=vector_config or self._default_vector_config, **kwargs
            )
            return True
        logger.warning("Collection %s already exists. Skipping.", collection_name)

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
        collection_name: str = None,
        wait: bool = True,
        ordering: WriteOrdering = WriteOrdering.MEDIUM,
        **kwargs,
    ) -> UpdateResult:
        if isinstance(points, dict):
            points = self.build_points(points)

        self.create_collection(collection_name or self.collection_name)

        result = self.client.upsert(
            collection_name=collection_name or self.collection_name,
            points=points,
            wait=wait,
            ordering=ordering,
            **kwargs,
        )
        logger.info(
            "Vectors upsert status: %(status)s. Operation ID: %(id)s",
            {"id": result.operation_id, "status": result.status},
        )
        return result
