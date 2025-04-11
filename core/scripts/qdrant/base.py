from abc import ABC, abstractmethod
from collections.abc import Iterable

from qdrant_client.http.models import PointStruct


class VectorWriter(ABC):
    """Abstract base class for vector writers."""

    @abstractmethod
    def upsert(self, points: Iterable[dict | PointStruct], **kwargs) -> None:
        """Upsert points into the vector storage."""
        pass


class VectorReader(ABC):
    """Abstract base class for vector readers."""

    @abstractmethod
    def search(self, query_vector: list[float], **filters) -> list[dict]:
        """Search for points in the vector storage."""
        pass


class VectorAsyncReader(ABC):
    """Abstract base class for vector readers."""

    @abstractmethod
    async def search(self, query_vector: list[float], **filters) -> list[dict]:
        """Search for points in the vector storage."""
        pass
