import sqlite3
from pathlib import Path


DB_PATH = Path("database/rag_analyzer.db")


def create_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            chunk_id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            page INTEGER NOT NULL,
            text TEXT NOT NULL,
            section TEXT
        )
    """)

    connection.commit()
    connection.close()


def insert_chunks(chunks):
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    for chunk in chunks:
        cursor.execute("""
            INSERT OR REPLACE INTO chunks
            (chunk_id, filename, page, text, section)
            VALUES (?, ?, ?, ?, ?)
        """, (
            chunk["chunk_id"],
            chunk["filename"],
            chunk["page"],
            chunk["text"],
            None
        ))

    connection.commit()
    connection.close()


def get_all_chunks():
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT chunk_id, filename, page, text, section
        FROM chunks
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


if __name__ == "__main__":
    from ingestion.pdf_loader import load_pdf
    from ingestion.chunker import create_chunks

    pdf_path = "data/raw/NIST_CSF_2.0.pdf"

    documents = load_pdf(pdf_path)
    chunks = create_chunks(documents)

    create_database()
    insert_chunks(chunks)

    stored_chunks = get_all_chunks()

    print(f"Pages loaded: {len(documents)}")
    print(f"Chunks created: {len(chunks)}")
    print(f"Chunks stored in SQLite: {len(stored_chunks)}")