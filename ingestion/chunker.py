def create_chunks(documents, chunk_size=1000, overlap=200):
    chunks = []

    chunk_number = 1

    for document in documents:
        text = document["text"]
        filename = document["filename"]
        page = document["page"]

        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "chunk_id": f"chunk_{chunk_number:04d}",
                    "text": chunk_text,
                    "filename": filename,
                    "page": page
                })

                chunk_number += 1

            start += chunk_size - overlap

    return chunks


if __name__ == "__main__":
    from pdf_loader import load_pdf

    pdf_path = "data/raw/NIST_CSF_2.0.pdf"

    documents = load_pdf(pdf_path)
    chunks = create_chunks(documents)

    print(f"Total pages: {len(documents)}")
    print(f"Total chunks: {len(chunks)}")

    for chunk in chunks[:3]:
        print("\n--------------------")
        print("Chunk ID:", chunk["chunk_id"])
        print("File:", chunk["filename"])
        print("Page:", chunk["page"])
        print("Text:", chunk["text"][:300])