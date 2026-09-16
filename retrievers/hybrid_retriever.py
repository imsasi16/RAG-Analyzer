from retrievers.keyword_retriever import create_fts_table, keyword_search
from retrievers.vector_retriever import vector_search


def hybrid_search(query, limit=5):

    # Get more candidates from both methods
    keyword_results = keyword_search(
        query,
        limit=10
    )

    vector_results = vector_search(
        query,
        limit=10
    )

    combined = {}

    # --------------------------------------------------
    # KEYWORD RESULTS
    # --------------------------------------------------

    for rank, result in enumerate(
        keyword_results,
        start=1
    ):

        chunk_id, filename, page, text = result

        combined[chunk_id] = {
            "chunk_id": chunk_id,
            "filename": filename,
            "page": page,
            "text": text,
            "keyword_rank": rank,
            "vector_rank": None
        }

    # --------------------------------------------------
    # VECTOR RESULTS
    # --------------------------------------------------

    ids = vector_results.get("ids", [[]])[0]
    documents = vector_results.get("documents", [[]])[0]
    metadatas = vector_results.get("metadatas", [[]])[0]

    for rank, chunk_id in enumerate(
        ids,
        start=1
    ):

        if chunk_id in combined:

            combined[chunk_id]["vector_rank"] = rank

        else:

            combined[chunk_id] = {
                "chunk_id": chunk_id,
                "filename": metadatas[rank - 1]["filename"],
                "page": metadatas[rank - 1]["page"],
                "text": documents[rank - 1],
                "keyword_rank": None,
                "vector_rank": rank
            }

    # --------------------------------------------------
    # RECIPROCAL RANK FUSION
    # --------------------------------------------------

    k = 60

    for result in combined.values():

        keyword_score = 0

        vector_score = 0

        if result["keyword_rank"] is not None:
            keyword_score = 1 / (
                k + result["keyword_rank"]
            )

        if result["vector_rank"] is not None:
            vector_score = 1 / (
                k + result["vector_rank"]
            )

        result["keyword_score"] = keyword_score
        result["vector_score"] = vector_score

        result["hybrid_score"] = (
            keyword_score + vector_score
        )

    # --------------------------------------------------
    # SORT BY HYBRID SCORE
    # --------------------------------------------------

    results = sorted(
        combined.values(),
        key=lambda x: x["hybrid_score"],
        reverse=True
    )

    return results[:limit]


if __name__ == "__main__":

    create_fts_table()

    query = input(
        "Search query: "
    )

    results = hybrid_search(
        query
    )

    print("\nHybrid Search")

    print(
        "Search query:",
        query
    )

    print(
        "Results found:",
        len(results)
    )

    for result in results:

        print("\n--------------------")

        print(
            "Chunk ID:",
            result["chunk_id"]
        )

        print(
            "File:",
            result["filename"]
        )

        print(
            "Page:",
            result["page"]
        )

        print(
            "Keyword rank:",
            result["keyword_rank"]
        )

        print(
            "Vector rank:",
            result["vector_rank"]
        )

        print(
            "Hybrid score:",
            round(
                result["hybrid_score"],
                6
            )
        )

        print(
            "Text:",
            result["text"][:300]
        )