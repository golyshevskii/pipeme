from typing import Any, Optional

from core.scripts.qdrant.client import QDRANT_CLIENT, QdrantClient
from logs.logger import get_logger
from qdrant_client.http.models import Distance, PointStruct, UpdateResult, VectorParams, WriteOrdering

logger = get_logger(__name__)


class QdrantManager:
    """
    Manager for Qdrant vector database.

    Attributes
    ----------
    client: The Qdrant client to use.
    """

    def __init__(self, client: QdrantClient):
        self.client = client

    def create_collection(
        self, collection_name: str, vector_size: int = 1024, distance: str = Distance.COSINE
    ) -> Optional[bool]:
        """
        Create a specific collection.

        Params
        ------
        collection_name: The name of the collection to create.
        vector_size: The size of the vector to use in the collection.
            It depends on the embedding model.
        distance: The distance of the vector.
            Use "Cosine" for text embedding and "Euclidean" for numerical embedding.

        Returns
        -------
        True if the collection was created.
        """
        if not self.client.collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=distance),
            )
            return True
        logger.warning("Collection %s already exists. Skipping.", collection_name)

    def delete_collection(self, collection_name: str) -> Optional[bool]:
        """
        Delete a collection.

        Params
        ------
        collection_name: The name of the collection to delete.

        Returns
        -------
        True if the collection was deleted.
        """
        if self.client.collection_exists(collection_name):
            self.client.delete_collection(collection_name=collection_name)
            return True
        logger.warning("Collection %s does not exist. Skipping.", collection_name)

    def upsert_vectors(
        self,
        collection_name: str,
        vectors: list[dict[str, Any]],
        wait: bool = False,
        ordering: WriteOrdering = WriteOrdering.MEDIUM,
    ) -> UpdateResult:
        """
        Upsert vectors into a collection.

        Params
        ------
        collection_name: The name of the collection to upsert the vectors into.
        vectors: The vectors to upsert.
        wait: Whether to wait for the operation to complete.
        ordering: The ordering of the operation.
            Use "WEAK" for better performance.
            Use "MEDIUM" for better performance and consistency.
            Use "STRONG" for better consistency.
        """
        self.create_collection(collection_name=collection_name)
        result = self.client.upsert(
            collection_name=collection_name, points=self.build_points(vectors), wait=wait, ordering=ordering
        )
        logger.info(
            "Vectors upsert status: %(status)s. Operation ID: %(id)s",
            {"id": result.operation_id, "status": result.status},
        )
        return result

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
            points.append(PointStruct(id=vid, vector=vector["vector"], payload=vector["payload"]))
            processed_ids.add(vid)
        logger.debug("Vectors points built. Amount: %s", len(points))
        return points


QDRANT_MANAGER = QdrantManager(QDRANT_CLIENT)
