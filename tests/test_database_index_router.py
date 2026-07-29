from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_existing_index():

    fake_documents = [
        {"table": "customers"},
        {"table": "orders"}
    ]

    with patch(
        "app.routers.database.IndexingService"
    ) as MockIndexingService:

        service = MockIndexingService.return_value

        service.index_exists.return_value = True
        service.load_index.return_value = fake_documents

        response = client.post(
            "/database/index",
            json={
                "host": "localhost",
                "port": 5432,
                "database": "northwind",
                "username": "postgres",
                "password": "test-password"
            }
        )

        assert response.status_code == 200

        data = response.json()

        assert data["success"] is True
        assert data["data"]["indexed_tables"] == 2
        assert data["data"]["reused"] is True

        service.index_exists.assert_called_once_with(
            "northwind"
        )

        service.load_index.assert_called_once_with(
            "northwind"
        )

        service.build_index.assert_not_called()


def test_missing_index():

    fake_documents = [
        {"table": "customers"},
        {"table": "orders"},
        {"table": "products"}
    ]

    with patch(
        "app.routers.database.IndexingService"
    ) as MockIndexingService:

        service = MockIndexingService.return_value

        service.index_exists.return_value = False
        service.build_index.return_value = fake_documents

        response = client.post(
            "/database/index",
            json={
                "host": "localhost",
                "port": 5432,
                "database": "new_database",
                "username": "postgres",
                "password": "test-password"
            }
        )

        assert response.status_code == 200

        data = response.json()

        assert data["success"] is True
        assert data["data"]["indexed_tables"] == 3
        assert data["data"]["reused"] is False

        service.index_exists.assert_called_once_with(
            "new_database"
        )

        service.build_index.assert_called_once()

        request = service.build_index.call_args.args[0]

        assert request.database == "new_database"

        service.load_index.assert_not_called()


def main():

    test_existing_index()

    print("Existing index reuse test passed.")

    test_missing_index()

    print("Missing index build test passed.")

    print("Database index router tests passed.")


if __name__ == "__main__":
    main()