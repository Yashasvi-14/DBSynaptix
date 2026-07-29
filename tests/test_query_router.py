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
        }
    ]

    fake_result = {
        "question": "List all customers",
        "sql": "SELECT * FROM customers;",
        "results": [
            {
                "customer_id": "ALFKI",
                "company_name": "Alfreds Futterkiste"
            }
        ],
        "repair_attempted": False,
        "repair_successful": False,
        "prompt_tokens": 100,
        "completion_tokens": 10,
        "total_tokens": 110
    }

    with patch(
        "app.routers.query.IndexingService"
    ) as MockIndexingService, patch(
        "app.routers.query.TextToSQLService"
    ) as MockTextToSQLService:

        # Mock persistent index loading
        indexing_service = MockIndexingService.return_value

        indexing_service.load_index.return_value = (
            fake_documents
        )

        # Mock Text-to-SQL pipeline
        text_to_sql_service = (
            MockTextToSQLService.return_value
        )

        text_to_sql_service.answer_question.return_value = (
            fake_result
        )

        payload = {
            "question": "List all customers",
            "database": {
                "host": "localhost",
                "port": 5432,
                "database": "northwind",
                "username": "postgres",
                "password": "test-password"
            }
        }

        response = client.post(
            "/query",
            json=payload
        )

        assert response.status_code == 200

        data = response.json()

        assert data["question"] == "List all customers"

        assert data["sql"] == (
            "SELECT * FROM customers;"
        )

        assert data["repair_attempted"] is False

        assert data["total_tokens"] == 110

        assert len(data["results"]) == 1

        # Persistent index must be loaded exactly once.
        indexing_service.load_index.assert_called_once_with(
            "northwind"
        )

        # Pipeline must receive the question,
        # parsed database request and loaded documents.
        text_to_sql_service.answer_question.assert_called_once()

        call = (
            text_to_sql_service
            .answer_question
            .call_args
        )

        assert call.kwargs["question"] == (
            "List all customers"
        )

        assert call.kwargs["documents"] == (
            fake_documents
        )

        assert (
            call.kwargs["request"].database
            == "northwind"
        )

    print("Query router test passed.")


if __name__ == "__main__":
    main()