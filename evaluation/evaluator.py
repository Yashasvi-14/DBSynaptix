import json
from pathlib import Path

from app.ai.retrieval import RetrievalEngine
from app.context.context_builder import ContextBuilder
from app.services.indexing_service import IndexingService


DATABASE_NAME = "northwind"
TOP_K = 3

QUESTIONS_PATH = Path("evaluation/questions.json")

RESULTS_PATH = Path("evaluation/results.json")

def load_questions():
    with open(QUESTIONS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def calculate_recall(expected_tables, actual_tables):
    expected = set(expected_tables)
    actual = set(actual_tables)

    if not expected:
        return 1.0

    return len(expected & actual) / len(expected)

def calculate_precision(expected_tables, actual_tables):
    expected = set(expected_tables)
    actual = set(actual_tables)

    if not actual:
        return 0.0

    return len(expected & actual) / len(actual)


def main():
    questions = load_questions()

    indexing_service = IndexingService()

    documents = indexing_service.load_index(
        DATABASE_NAME
    )

    retriever = RetrievalEngine()
    context_builder = ContextBuilder()

    print(f"Loaded {len(documents)} indexed tables")
    print(f"Loaded {len(questions)} benchmark questions")
    print()

    results = []
    for benchmark in questions:
        question = benchmark["question"]
        expected_tables = benchmark["expected_tables"]

        retrieval_results = retriever.retrieve(
            documents,
            question
        )

        if benchmark["id"] in {"B011", "B019"}:
            print()
            print(f"FULL RANKING — {benchmark['id']}")

            for rank, result in enumerate(
                retrieval_results,
                start=1
            ):
                print(
                    rank,
                    result["table"],
                    f"final={result['final_score']:.4f}",
                    f"keyword={result['keyword_score']:.4f}",
                    f"semantic={result['semantic_score']:.4f}"
                )

            print()

        initial_tables = [
            result["table"]
            for result in retrieval_results[:TOP_K]
        ]

        context = context_builder.expand(
            retrieval_results,
            documents,
            top_k=TOP_K
        )

        context_tables = [
            document["table"]
            for document in context
        ]

        retrieval_recall = calculate_recall(
            expected_tables,
            initial_tables
        )

        context_recall = calculate_recall(
            expected_tables,
            context_tables
        )

        context_precision = calculate_precision(
            expected_tables,
            context_tables
        )

        context_ratio = (
            len(context_tables) / len(documents)
            if documents
            else 0
        )

        results.append({
            "id": benchmark["id"],
            "difficulty": benchmark["difficulty"],
            "category": benchmark["category"],
            "question": question,

            "expected_tables": expected_tables,
            "retrieved_tables": initial_tables,
            "context_tables": context_tables,

            "retrieval_recall": retrieval_recall,
            "context_recall": context_recall,

            "context_table_count": len(context_tables),
            "total_table_count": len(documents),
            "context_ratio": context_ratio,

            "context_precision": context_precision,
        })

        print("=" * 70)
        print(f"{benchmark['id']} | {benchmark['difficulty']}")
        print(question)

        print(f"Expected : {expected_tables}")
        print(f"Retrieved: {initial_tables}")
        print(f"Context  : {context_tables}")

        print(
            f"Retrieval Recall: {retrieval_recall:.2%}"
        )

        print(
            f"Context Recall:   {context_recall:.2%}"
        )

        print(
            f"Context Ratio:    {context_ratio:.2%}"
        )

        print(
            f"Context Precision: {context_precision:.2%}"
        )

    with open(
        RESULTS_PATH,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            results,
            file,
            indent=2
        )

    print()
    print(
        f"Saved benchmark results to {RESULTS_PATH}"
    )


if __name__ == "__main__":
    main()