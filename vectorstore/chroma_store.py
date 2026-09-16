import chromadb
from pathlib import Path

from ingestion.pdf_loader import load_pdf
from ingestion.chunker import create_chunks
from vectorstore.embeddings import load_embedding_model


CHROMA_PATH = Path("vectorstore/chroma_db")
DATA_PATH = Path("data/raw")


def create_vector_store():

    # Find all PDF files
    pdf_files = list(DATA_PATH.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in data/raw/")
        return

    print("PDF files found:", len(pdf_files))

    all_chunks = []

    # Process every PDF
    for pdf_path in pdf_files:

        print(f"\nProcessing: {pdf_path.name}")

        documents = load_pdf(str(pdf_path))
        chunks = create_chunks(documents)

        all_chunks.extend(chunks)

        print("Chunks created:", len(chunks))

    # Load embedding model once
    model = load_embedding_model()

    texts = [chunk["text"] for chunk in all_chunks]

    print("\nCreating embeddings...")

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    # Connect to ChromaDB
    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH)
    )

    collection = client.get_or_create_collection(
        name="rag_analyzer"
    )

    # Store everything
    collection.upsert(
        ids=[chunk["chunk_id"] for chunk in all_chunks],
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=[
            {
                "filename": chunk["filename"],
                "page": chunk["page"]
            }
            for chunk in all_chunks
        ]
    )

    print("\nVector store created successfully.")
    print("Total chunks stored:", collection.count())


if __name__ == "__main__":
    create_vector_store()