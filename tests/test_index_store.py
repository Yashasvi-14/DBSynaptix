import tempfile
from pathlib import Path

from app.indexing.index_store import IndexStore


def main():

    documents = [
        {
            "table": "customers",
            "text": "TABLE: customers",
            "embedding": [0.1, 0.2, 0.3],
            "structured": {
                "columns": [
                    "customer_id",
                    "contact_name"
                ],
                "foreign_keys": []
            }
        },
        {
            "table": "orders",
            "text": "TABLE: orders",
            "embedding": [0.4, 0.5, 0.6],
            "structured": {
                "columns": [
                    "order_id",
                    "customer_id"
                ],
                "foreign_keys": []
            }
        }
    ]

    # Use a temporary directory so the test does not
    # create data/index.json.
    with tempfile.TemporaryDirectory() as temp_dir:

        index_path = (
            Path(temp_dir)
            / "index.json"
        )

        store = IndexStore(
            path=index_path
        )

        # Index should not exist initially.
        assert store.exists() is False

        # Save index.
        store.save(documents)

        assert store.exists() is True

        # Load it again.
        loaded_documents = store.load()

        assert loaded_documents == documents

        assert (
            loaded_documents[0]["embedding"]
            == [0.1, 0.2, 0.3]
        )

        assert (
            loaded_documents[1]["table"]
            == "orders"
        )

    print("IndexStore test passed.")


if __name__ == "__main__":
    main()