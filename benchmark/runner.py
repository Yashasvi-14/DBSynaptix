import json
from benchmark.config import QUESTIONS_PATH
from app.services.text_to_sql_service import TextToSQLService


class BenchmarkRunner:

    def __init__(self, dataset="northwind"):
        self.questions_path = QUESTIONS_PATH
        self.service = TextToSQLService()

    def load_questions(self):
        with open(self.questions_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def run(self):
        questions = self.load_questions()

        print(f"Loaded {len(questions)} benchmark questions.\n")

        for question in questions:
            if not question["enabled"]:
                continue

            print(f'{question["id"]}: {question["question"]}')


if __name__ == "__main__":
    runner = BenchmarkRunner()
    runner.run()

