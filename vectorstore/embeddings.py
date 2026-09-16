from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


def load_embedding_model():
    return SentenceTransformer(MODEL_NAME)


def create_embeddings(texts):
    model = load_embedding_model()

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    return embeddings


if __name__ == "__main__":
    sample_texts = [
        "Cybersecurity risk management",
        "Protecting user accounts"
    ]

    embeddings = create_embeddings(sample_texts)

    print("Number of texts:", len(embeddings))
    print("Embedding size:", len(embeddings[0]))