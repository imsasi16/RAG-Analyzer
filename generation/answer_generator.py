from generation.llm import generate_answer
from groq import APIError

ANSWER_NOT_FOUND = "The answer could not be found in the provided document."
ANSWER_GENERATION_ERROR = "Unable to generate an answer right now."


def build_context(results):

    context_parts = []

    for result in results:

        if isinstance(result, dict):

            filename = result["filename"]
            page = result["page"]
            text = result["text"]

        else:

            filename = result[1]
            page = result[2]
            text = result[3]

        context_parts.append(
            f"Source: {filename}, Page: {page}\n"
            f"{text}"
        )

    return "\n\n".join(context_parts)


def generate_rag_answer(question, results):

    if not results:
        return ANSWER_NOT_FOUND

    context = build_context(results)

    prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the
provided document context.

Rules:

1. Do not use outside knowledge.
2. Do not invent information.
3. If the answer is not present in the context, say exactly:
"The answer could not be found in the provided document."

4. Give a clear and concise answer.
5. Base the answer only on the retrieved context.
6. Do not mention retrieval methods.
7. Do not mention that you are an AI.
8. Do not mention embeddings, vectors, chunks, algorithms, models,
   prompts, scores, ranks, distances, or retrieval.
9. Write 2 to 4 short sentences when the context supports an answer.

User question:
{question}

Document context:
{context}

Answer:
"""

    try:
        return generate_answer(prompt)
    except APIError:
        return ANSWER_GENERATION_ERROR