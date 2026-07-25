from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET = "northwind"

QUESTIONS_PATH = (
    PROJECT_ROOT
    / "benchmark"
    / "datasets"
    / DATASET
    / "questions.json"
)