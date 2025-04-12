import asyncio
from datetime import datetime, timezone

from core.scripts.qdrant.client import get_qdrant_client
from core.scripts.qdrant.sync.manager import QdrantSyncManager
from core.scripts.embedding.manager import EMBEDDING_MANAGER


async def build_vectors(data: list[str]) -> list[dict]:
    vectors = []
    for i, data in enumerate(data):
        vectors.append(
            {
                "id": i,
                "vector": await EMBEDDING_MANAGER.vectorize(data),
                "payload": {
                    "source": "Confluence",
                    "content": data,
                    "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f"),
                }
            }
        )
    return vectors


async def upsert_vectors(vectors: list[dict], collection_name: str) -> None:
    qdrant_sync_manager = QdrantSyncManager(collection_name)
    qdrant_sync_manager.upsert(vectors)


async def main():
    data = [
        "Trades by month can be found in dwh.raw.trades_by_month table.",
        "Trades by day can be found in dwh.raw.trades_by_day table.",
        "Trades by hour can be found in dwh.raw.trades_by_hour table.",
    ]

    collection_name = "docs"
    vectors = await build_vectors(data)
    await upsert_vectors(vectors, collection_name)

    async_qdrant_client = get_qdrant_client(async_client=True)

    request = "Where can I find trades by month?"
    query_vector = await EMBEDDING_MANAGER.vectorize(request)
    result = await async_qdrant_client.query_points(
        collection_name=collection_name,
        query=query_vector,
        score_threshold=0.7,
        limit=3,
    )

    print("Request:", request, "\nResult:", result.points[0].payload["content"])
    # Request: Where can I find trades by month?
    # Result: Trades by month can be found in dwh.raw.trades_by_month table.


if __name__ == "__main__":
    # python -m docs.examples.search_trades
    asyncio.run(main())
