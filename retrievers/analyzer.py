import sys

from retrievers.database_retriever import database_search
from retrievers.keyword_retriever import create_fts_table, keyword_search
from retrievers.metadata_retriever import metadata_search
from retrievers.vector_retriever import vector_search
from retrievers.hybrid_retriever import hybrid_search
from generation.answer_generator import ANSWER_NOT_FOUND, generate_rag_answer


METHODS = (
    ("DB BASELINE", "database"),
    ("KEYWORD RETRIEVAL", "keyword"),
    ("METADATA RETRIEVAL", "metadata"),
    ("VECTOR RETRIEVAL", "vector"),
    ("HYBRID RETRIEVAL", "hybrid"),
)


def convert_vector_results(results):
    converted = []
    ids = results.get("ids", [[]])[0]
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    for i, chunk_id in enumerate(ids):
        converted.append({
            "chunk_id": chunk_id,
            "filename": metadatas[i]["filename"],
            "page": metadatas[i]["page"],
            "text": documents[i],
        })

    return converted


def analyze_query(query, limit=5):
    """Run the same question through every retrieval method."""
    database_results = database_search(query=query, limit=limit)
    keyword_results = keyword_search(query, limit=limit)
    metadata_results = metadata_search(
        query=query,
        filename="NIST_CSF_2.0.pdf",
        limit=limit,
    )
    vector_results = convert_vector_results(vector_search(query, limit=limit))
    hybrid_results = hybrid_search(query, limit=limit)

    return {
        "database": database_results,
        "keyword": keyword_results,
        "metadata": metadata_results,
        "vector": vector_results,
        "hybrid": hybrid_results,
    }


def get_page_list(results):
    pages = []
    for result in results:
        page = result["page"] if isinstance(result, dict) else result[2]
        if page not in pages:
            pages.append(page)
    return sorted(pages)


def get_sources(results):
    filenames = []
    for result in results:
        filename = result["filename"] if isinstance(result, dict) else result[1]
        if filename not in filenames:
            filenames.append(filename)
    return filenames, get_page_list(results)


def generate_all_answers(question, results):
    answers = {}
    for name, key in METHODS:
        answers[key] = generate_rag_answer(question, results[key])
    return answers


def _print_method(number, name, answer, results):
    filenames, pages = get_sources(results)
    print(f"\n{number}. {name}\n")
    print("---")
    print("Answer:")
    print(answer)
    print("\nSource:")
    if filenames:
        print(", ".join(filenames))
        label = "Page" if len(pages) == 1 else "Pages"
        print(f"{label}: {', '.join(str(page) for page in pages)}")
    else:
        print("No document source found.")


def print_comparison(results, answers):
    print("\n" + "#" * 50)
    print("SIMPLE COMPARISON")
    print("\nMethod                 Answer Found  Source")
    for name, key in METHODS:
        _, pages = get_sources(results[key])
        found = answers[key] != ANSWER_NOT_FOUND
        source = ", ".join(str(page) for page in pages) if pages else "None"
        print(f"{name.title():<22} {'Yes' if found else 'No':<13} {source}")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    create_fts_table()
    print("#" + " " * 48 + "#")
    print("RAG ANALYZER")
    print("#" + " " * 48 + "#")

    query = input("\nAsk a question: ").strip()
    if not query:
        print("Question cannot be empty. Please enter a question.")
        return

    print("\nQuestion:")
    print(query)
    results = analyze_query(query)
    answers = generate_all_answers(query, results)

    for number, (name, key) in enumerate(METHODS, start=1):
        _print_method(number, name, answers[key], results[key])
    print_comparison(results, answers)


if __name__ == "__main__":
    main()
