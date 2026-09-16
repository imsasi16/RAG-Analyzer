import sqlite3
from pathlib import Path
import re


DB_PATH = Path("database/rag_analyzer.db")


def create_fts_table():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS chunks_fts")

    cursor.execute("""
        CREATE VIRTUAL TABLE chunks_fts
        USING fts5(
            chunk_id,
            filename,
            page UNINDEXED,
            text
        )
    """)

    cursor.execute("""
        INSERT INTO chunks_fts(chunk_id, filename, page, text)
        SELECT chunk_id, filename, page, text
        FROM chunks
    """)

    connection.commit()
    connection.close()


def keyword_search(query, limit=5):

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Convert a natural-language question into safe search words
    words = re.findall(r"[A-Za-z0-9_]+", query)

    # Remove very short words
    words = [
        word for word in words
        if len(word) > 2
    ]

    if not words:
        connection.close()
        return []

    # Example:
    # "What is cybersecurity risk management?"
    # becomes:
    # "What OR cybersecurity OR risk OR management"
    fts_query = " OR ".join(words)

    try:
        cursor.execute("""
            SELECT chunk_id, filename, page, text
            FROM chunks_fts
            WHERE chunks_fts MATCH ?
            LIMIT ?
        """, (fts_query, limit))
    except sqlite3.OperationalError:
        # Evaluation should be read-only; use the source table if FTS has
        # not been initialized by the interactive analyzer yet.
        conditions = " OR ".join(["text LIKE ?" for _ in words])
        cursor.execute(
            f"""
            SELECT chunk_id, filename, page, text
            FROM chunks
            WHERE {conditions}
            LIMIT ?
            """,
            tuple(f"%{word}%" for word in words) + (limit,)
        )

    results = cursor.fetchall()

    connection.close()

    return results


if __name__ == "__main__":

    create_fts_table()

    query = "What is cybersecurity risk management?"

    results = keyword_search(query)

    print(f"Search query: {query}")
    print(f"Results found: {len(results)}")

    for result in results:

        chunk_id, filename, page, text = result

        print("\n--------------------")
        print("Chunk ID:", chunk_id)
        print("File:", filename)
        print("Page:", page)
        print("Text:", text[:500])