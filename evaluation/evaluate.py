import json
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from generation.answer_generator import generate_rag_answer
from retrievers.analyzer import METHODS, analyze_query, get_page_list


DATASET_PATH = Path(__file__).with_name("eval_dataset.json")
RESULTS_PATH = Path(__file__).with_name("results.json")
REPORT_PATH = Path(__file__).with_name("RESULTS.md")


def result_text(result):
    return result["text"] if isinstance(result, dict) else result[3]


def relevant_context(results, keywords):
    text = " ".join(result_text(result) for result in results).lower()
    return any(keyword.lower() in text for keyword in keywords)


def evaluate_question(item):
    question = item["question"]
    keywords = item.get("keywords", [])
    retrievals = analyze_query(question)
    records = []

    for method_name, key in METHODS:
        started = time.perf_counter()
        method_results = retrievals[key]
        answer = generate_rag_answer(question, method_results)
        elapsed = time.perf_counter() - started
        records.append({
            "question": question,
            "retrieval_method": method_name,
            "answer": answer,
            "source_pages": get_page_list(method_results),
            "relevant_context_retrieved": relevant_context(
                method_results, keywords
            ),
            "execution_time_seconds": round(elapsed, 6),
        })

    return records


def write_report(records):
    lines = [
        "# Evaluation Results",
        "",
        "| Question | Method | Relevant context | Pages | Time (s) |",
        "|---|---|---:|---|---:|",
    ]
    for record in records:
        question = record["question"].replace("|", "\\|")
        pages = ", ".join(str(page) for page in record["source_pages"]) or "None"
        relevant = "Yes" if record["relevant_context_retrieved"] else "No"
        lines.append(
            f"| {question} | {record['retrieval_method']} | "
            f"{relevant} | {pages} | {record['execution_time_seconds']:.3f} |"
        )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    questions = json.loads(DATASET_PATH.read_text(encoding="utf-8"))
    records = []
    for item in questions:
        records.extend(evaluate_question(item))

    RESULTS_PATH.write_text(
        json.dumps(records, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    write_report(records)
    print(f"Evaluated {len(questions)} questions across {len(METHODS)} methods.")
    print(f"Saved {RESULTS_PATH}")
    print(f"Saved {REPORT_PATH}")


if __name__ == "__main__":
    main()
