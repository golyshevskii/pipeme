import asyncio

from core.scripts.qdrant.manager import QDRANT_MANAGER
from core.scripts.qdrant.client import AQDRANT_CLIENT
from core.scripts.embedding.manager import EMBEDDING_MANAGER


async def main():
    data = [
        "Trades by month can be found in pipeme.raw.trades_by_month table",
        "Trades by day can be found in pipeme.raw.trades_by_day table",
        "Trades by hour can be found in pipeme.raw.trades_by_hour table",
    ]

    vectors = []
    for i, data in enumerate(data):
        vectors.append(
            {
                "id": i,
                "vector": await EMBEDDING_MANAGER.vectorize(data),
                "payload": {
                    "source": "DWH",
                    "project": "pipeme",
                    "dataset": "raw",
                    "text": data,
                }
            }
        )

    QDRANT_MANAGER.upsert_vectors(
        collection_name="pipeme",
        vectors=vectors,
    )

    request = "What is the total volume of trades by month?"
    vector = await EMBEDDING_MANAGER.vectorize(request)
    result = await AQDRANT_CLIENT.query_points(
        collection_name="pipeme",
        query=vector,
        score_threshold=0.7,
        limit=3,
    )

    print("Request:", request, "\nResult:", result.points[0].payload["text"])
    # Request: What is the total volume of trades by month? 
    # Result: Trades by month can be found in pipeme.raw.trades_by_month table


if __name__ == "__main__":
    asyncio.run(main())
