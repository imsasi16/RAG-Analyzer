from pathlib import Path
from pypdf import PdfReader


def load_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        documents.append({
            "filename": Path(pdf_path).name,
            "page": page_number,
            "text": text
        })

    return documents


if __name__ == "__main__":
    pdf_path = "data/raw/NIST_CSF_2.0.pdf"

    documents = load_pdf(pdf_path)

    print(f"Total pages: {len(documents)}")

    for document in documents[:2]:
        print("\n--- Page", document["page"], "---")
        print(document["text"][:500])