import csv
import json
import time

from app.services.text_to_sql_service import TextToSQLService

from app.services.indexing_service import IndexingService

from app.schemas.database import DatabaseConnectionRequest

from app.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)


def load_questions():
    with open(
        "benchmark/datasets/northwind/questions.json",
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def main():

    # ==========================================================
    # Database Connection
    # ==========================================================

    request = DatabaseConnectionRequest(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        username=DB_USER,
        password=DB_PASSWORD
    )

    # ==========================================================
    # Load Persistent Index
    # ==========================================================

    print("=" * 80)
    print("LOADING PERSISTENT INDEX")
    print("=" * 80)

    indexing_service = IndexingService()

    documents = indexing_service.load_index()

    print(
        f"\nPersistent index loaded successfully "
        f"({len(documents)} documents).\n"
    )
    

    # ==========================================================
    # Initialize Text-to-SQL Service
    # ==========================================================

    service = TextToSQLService()

    # ==========================================================
    # Load Benchmark Questions
    # ==========================================================

    benchmark_questions = load_questions()

    # ==========================================================
    # Benchmark Variables
    # ==========================================================

    total = 0
    success = 0

    results = []

    # ==========================================================
    # Run Benchmark
    # ==========================================================

    for item in benchmark_questions[19:20]:

        if not item["enabled"]:
            continue

        total += 1

        question = item["question"]

        print("=" * 100)
        print(f'{item["id"]} | {item["category"]} | {item["difficulty"]}')
        print(f"QUESTION : {question}")
        print("=" * 100)

        start = time.perf_counter()

        try:

            response = service.answer_question(
                question,
                request,
                documents
            )

            end = time.perf_counter()

            latency_ms = round((end - start) * 1000, 2)

            success += 1

            print("\nGenerated SQL\n")
            print(response["sql"])

            print("\nResults\n")

            for row in response["results"]:
                print(row)

            print(f"\nLatency : {latency_ms} ms")

            results.append({
                "id": item["id"],
                "category": item["category"],
                "difficulty": item["difficulty"],
                "question": question,
                "sql": response["sql"],
                "success": True,
                "latency_ms": latency_ms,
                "prompt_tokens": response["prompt_tokens"],
                "completion_tokens": response["completion_tokens"],
                "total_tokens": response["total_tokens"]
            })

        except Exception as e:

            end = time.perf_counter()

            latency_ms = round((end - start) * 1000, 2)

            print(f"\nFAILED : {e}")
            print(f"Latency : {latency_ms} ms")

            results.append({
                "id": item["id"],
                "category": item["category"],
                "difficulty": item["difficulty"],
                "question": question,
                "sql": "",
                "success": False,
                "latency_ms": latency_ms,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            })

        print("\n\n")

    # ==========================================================
    # Save Results
    # ==========================================================

    with open(
        "benchmark/results.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "id",
                "category",
                "difficulty",
                "question",
                "sql",
                "success",
                "latency_ms",
                "prompt_tokens",
                "completion_tokens",
                "total_tokens"
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    # ==========================================================
    # Benchmark Summary
    # ==========================================================

    print("=" * 100)
    print("BENCHMARK SUMMARY")
    print("=" * 100)

    print(f"Questions Run : {total}")
    print(f"Successful    : {success}")
    print(f"Failed        : {total - success}")

    print("\n✓ Results saved to benchmark/results.csv")


if __name__ == "__main__":
    main()