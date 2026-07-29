from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def main():

    fake_documents = [
        {
            "table": "customers",
            "text": "TABLE: customers",
            "embedding": [0.1, 0.2, 0.3]
        },
        {
            "table": "orders",
            "text": "TABLE: orders",
            "embedding": [0.4, 0.5, 0.6]
        }
    ]

    with patch(
        "app.routers.database.IndexingService"
    ) as MockIndexingService:

        indexing_service = (
            MockIndexingService.return_value
        )

        indexing_service.build_index.return_value = (
            fake_documents
        )

        payload = {
            "host": "localhost",
            "port": 5432,
            "database": "northwind",
            "username": "postgres",
            "password": "test-password"
        }

        response = client.post(
            "/database/index",
            json=payload
        )

        assert response.status_code == 200

        data = response.json()

        assert data["success"] is True

        assert (
            data["message"]
            == "Database indexed successfully"
        )

        assert data["data"]["indexed_tables"] == 2

        indexing_service.build_index.assert_called_once()

        call = (
            indexing_service
            .build_index
            .call_args
        )

        request = call.args[0]

        assert request.host == "localhost"
        assert request.port == 5432
        assert request.database == "northwind"
        assert request.username == "postgres"

    print("Database index router test passed.")


if __name__ == "__main__":
    main()