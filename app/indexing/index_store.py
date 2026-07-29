import json
from pathlib import Path


class IndexStore:
    """
    Persists and loads database retrieval documents.

    The stored index contains:
    - table metadata
    - semantic knowledge
    - retrieval text
    - embeddings
    """

    def __init__(
        self,
        path="data/index.json"
    ):
        self.path = Path(path)

    def save(
        self,
        documents
    ):
        """
        Persist indexed documents to disk.
        """

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                documents,
                file,
                indent=2
            )

    def load(self):
        """
        Load indexed documents from disk.
        """

        if not self.path.exists():
            raise FileNotFoundError(
                f"Index not found: {self.path}"
            )

        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def exists(self):
        """
        Check whether an index has been persisted.
        """

        return self.path.exists()