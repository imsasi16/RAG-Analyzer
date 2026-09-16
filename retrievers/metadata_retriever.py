import sqlite3
from pathlib import Path


DB_PATH = Path("database/rag_analyzer.db")


def metadata_search(query=None, page_number=None, filename=None, limit=5):

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    query = """
        SELECT chunk_id, filename, page, text
        FROM chunks
        WHERE 1=1
    """

    parameters = []

    if page_number is not None:
        query += " AND page = ?"
        parameters.append(page_number)

    if filename is not None:
        query += " AND filename = ?"
        parameters.append(filename)

    query += " LIMIT ?"
    parameters.append(limit)

    cursor.execute(query, parameters)

    results = cursor.fetchall()

    connection.close()

    return results


if __name__ == "__main__":

    filename = "NIST_CSF_2.0.pdf"
    page_number = 29

    results = metadata_search(
        page_number=page_number,
        filename=filename
    )

    print("Metadata search")
    print("Filename:", filename)
    print("Page:", page_number)
    print("Results found:", len(results))

    for result in results:

        chunk_id, filename, page, text = result

        print("\n--------------------")

        print("Chunk ID:", chunk_id)
        print("File:", filename)
        print("Page:", page)
        print("Text:", text[:500])