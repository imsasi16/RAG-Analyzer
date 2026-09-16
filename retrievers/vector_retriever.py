import chromadb
from pathlib import Path

from vectorstore.embeddings import load_embedding_model


CHROMA_PATH = Path("vectorstore/chroma_db")


def vector_search(query, limit=5):

    model = load_embedding_model()

    query_embedding = model.encode([query])[0].tolist()

    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH)
    )

    collection = client.get_collection(
        name="rag_analyzer"
    )

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=limit
    )

    return results


if __name__ == "__main__":

    query = "What is cybersecurity risk management?"

    results = vector_search(query)

    print("Search query:", query)
    print("Results found:", len(results["ids"][0]))

    for i in range(len(results["ids"][0])):

        print("\n--------------------")

        print("Chunk ID:", results["ids"][0][i])

        print("Page:", results["metadatas"][0][i]["page"])

        print("Distance:", results["distances"][0][i])

        print("Text:", results["documents"][0][i][:500])