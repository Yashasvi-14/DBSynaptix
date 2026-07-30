import json
import os
from pathlib import Path
from time import perf_counter

from dotenv import load_dotenv

from app.schemas.database import DatabaseConnectionRequest
from app.services.indexing_service import IndexingService
from app.services.text_to_sql_service import TextToSQLService


QUESTIONS_PATH = Path("evaluation/questions.json")
RESULTS_PATH = Path("evaluation/e2e_results.json")

TEST_IDS = {
    "B001",
    "B002",
    "B003",
    "B004",
    "B005",
}


def load_questions():
    with open(
        QUESTIONS_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def load_database_request():
    load_dotenv()

    required_variables = [
        "BENCHMARK_DB_HOST",
        "BENCHMARK_DB_PORT",
        "BENCHMARK_DB_NAME",
        "BENCHMARK_DB_USERNAME",
        "BENCHMARK_DB_PASSWORD",
    ]

    missing = [
        variable
        for variable in required_variables
        if not os.getenv(variable)
    ]

    if missing:
        raise RuntimeError(
            "Missing benchmark environment variables: "
            + ", ".join(missing)
        )

    return DatabaseConnectionRequest(
        host=os.environ["BENCHMARK_DB_HOST"],
        port=int(os.environ["BENCHMARK_DB_PORT"]),
        database=os.environ["BENCHMARK_DB_NAME"],
        username=os.environ["BENCHMARK_DB_USERNAME"],
        password=os.environ["BENCHMARK_DB_PASSWORD"],
    )

def normalize_results(rows):
    return sorted(
        [tuple(row.values()) for row in rows],
        key=repr
    )

def main():
    questions = load_questions()
    database = load_database_request()

    indexing_service = IndexingService()

    documents = indexing_service.load_index(
        database.database
    )

    service = TextToSQLService()

    benchmark_results = []

    selected_questions = [
        benchmark
        for benchmark in questions
        if benchmark["id"] in TEST_IDS
    ]

    print(
        f"Running {len(selected_questions)} "
        "end-to-end benchmark case(s)"
    )
    print()

    for benchmark in selected_questions:

        print("=" * 70)
        print(
            f"{benchmark['id']} | "
            f"{benchmark['difficulty']}"
        )
        print(benchmark["question"])

        benchmark_start = perf_counter()

        try:
            result = service.answer_question(
                question=benchmark["question"],
                request=database,
                documents=documents
            )

            expected_results = service.executor.execute(
                benchmark["ground_truth_sql"],
                database
            )

            result_correct = (
                normalize_results(result["results"])
                ==
                normalize_results(expected_results)
            )

            benchmark_result = {
                "id": benchmark["id"],
                "difficulty": benchmark["difficulty"],
                "category": benchmark["category"],
                "question": benchmark["question"],
                "result_correct": result_correct,
                "execution_success": True,
                "error": None,

                "sql": result["sql"],
                "row_count": len(result["results"]),

                "repair_attempted": (
                    result["repair_attempted"]
                ),
                "repair_successful": (
                    result["repair_successful"]
                ),

                "prompt_tokens": result["prompt_tokens"],
                "completion_tokens": (
                    result["completion_tokens"]
                ),
                "total_tokens": result["total_tokens"],

                "timings": result["timings"],
            }

            print("Execution: SUCCESS")
            print(
                f"Correct:   {result_correct}"
            )
            print(f"Rows:      {len(result['results'])}")
            print(
                f"Repair:    "
                f"{result['repair_attempted']}"
            )
            print(
                f"Tokens:    {result['total_tokens']}"
            )
            print(
                f"Total:     "
                f"{result['timings']['total_ms']:.2f} ms"
            )

        except Exception as error:

            elapsed_ms = round(
                (perf_counter() - benchmark_start) * 1000,
                2
            )

            benchmark_result = {
                "id": benchmark["id"],
                "difficulty": benchmark["difficulty"],
                "category": benchmark["category"],
                "question": benchmark["question"],

                "execution_success": False,
                "error": (
                    f"{type(error).__name__}: {error}"
                ),

                "sql": None,
                "row_count": None,

                "repair_attempted": None,
                "repair_successful": None,

                "prompt_tokens": None,
                "completion_tokens": None,
                "total_tokens": None,

                "timings": {
                    "total_ms": elapsed_ms
                },
            }

            print("Execution: FAILED")
            print(
                f"Error:     "
                f"{type(error).__name__}: {error}"
            )

        benchmark_results.append(
            benchmark_result
        )

    with open(
        RESULTS_PATH,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            benchmark_results,
            file,
            indent=2,
            default=str
        )

    print()
    print(
        f"Saved results to {RESULTS_PATH}"
    )


if __name__ == "__main__":
    main()