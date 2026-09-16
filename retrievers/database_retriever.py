import sqlite3
from pathlib import Path


DB_PATH = Path("database/rag_analyzer.db")


def database_search(query=None, limit=5):

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT chunk_id, filename, page, text
        FROM chunks
        LIMIT ?
    """, (limit,))

    results = cursor.fetchall()

    connection.close()

    return results


if __name__ == "__main__":

    results = database_search()

    print("Normal DB search")
    print("Results found:", len(results))

    for result in results:

        chunk_id, filename, page, text = result

        print("\n--------------------")
        print("Chunk ID:", chunk_id)
        print("File:", filename)
        print("Page:", page)
        print("Text:", text[:500])