import json
from collections import defaultdict
from pathlib import Path


RESULTS_PATH = Path("evaluation/results.json")
SUMMARY_PATH = Path("evaluation/summary.json")


def load_results():
    with open(RESULTS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def average(values):
    if not values:
        return 0

    return sum(values) / len(values)


def summarize_group(results):
    return {
        "questions": len(results),

        "retrieval_recall": average([
            result["retrieval_recall"]
            for result in results
        ]),

        "context_recall": average([
            result["context_recall"]
            for result in results
        ]),

        "context_ratio": average([
            result["context_ratio"]
            for result in results
        ]),

        "perfect_retrieval_cases": sum(
            result["retrieval_recall"] == 1.0
            for result in results
        ),

        "perfect_context_cases": sum(
            result["context_recall"] == 1.0
            for result in results
        ),

        "context_precision": average([
            result["context_precision"]
            for result in results
        ]), 
    }


def main():
    results = load_results()

    difficulty_groups = defaultdict(list)
    category_groups = defaultdict(list)

    for result in results:
        difficulty_groups[
            result["difficulty"]
        ].append(result)

        category_groups[
            result["category"]
        ].append(result)

    summary = {
        "overall": summarize_group(results),

        "by_difficulty": {
            difficulty: summarize_group(group)
            for difficulty, group
            in difficulty_groups.items()
        },

        "by_category": {
            category: summarize_group(group)
            for category, group
            in category_groups.items()
        }
    }

    with open(
        SUMMARY_PATH,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            summary,
            file,
            indent=2
        )

    overall = summary["overall"]

    print("DBSynaptix Retrieval Benchmark")
    print("=" * 40)

    print(
        f"Questions:         {overall['questions']}"
    )

    print(
        "Retrieval Recall:  "
        f"{overall['retrieval_recall']:.2%}"
    )

    print(
        "Context Recall:    "
        f"{overall['context_recall']:.2%}"
    )

    print(
        "Context Ratio:     "
        f"{overall['context_ratio']:.2%}"
    )

    print(
        "Perfect Retrieval: "
        f"{overall['perfect_retrieval_cases']}"
        f"/{overall['questions']}"
    )

    print(
        "Perfect Context:   "
        f"{overall['perfect_context_cases']}"
        f"/{overall['questions']}"
    )

    print(
        "Context Precision: "
        f"{overall['context_precision']:.2%}"
    )

    print()
    print(f"Saved summary to {SUMMARY_PATH}")


if __name__ == "__main__":
    main()