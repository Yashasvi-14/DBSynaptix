from unittest.mock import MagicMock

from app.services.indexing_service import IndexingService


def main():

    service = IndexingService()

    # Fake database request
    request = MagicMock()
    request.database = "northwind"

    # Fake database-specific index store
    mock_store = MagicMock()

    service.get_index_store = MagicMock(
        return_value=mock_store
    )

    # ==========================================================
    # Fake pipeline data
    # ==========================================================

    schema = {
        "customers": {
            "columns": []
        }
    }

    knowledge = {
        "customers": {
            "summary": "Customer information"
        }
    }

    documents = [
        {
            "table": "customers",
            "text": "TABLE: customers"
        }
    ]

    embedded_documents = [
        {
            "table": "customers",
            "text": "TABLE: customers",
            "embedding": [0.1, 0.2, 0.3]
        }
    ]

    # ==========================================================
    # Mock indexing stages
    # ==========================================================

    schema_response = MagicMock()
    schema_response.data = schema

    service.database_service.get_schema = MagicMock(
        return_value=schema_response
    )

    service.knowledge_builder.build_database_knowledge = MagicMock(
        return_value=knowledge
    )

    service.document_builder.build = MagicMock(
        return_value=documents
    )

    service.embedding_builder.build_embeddings = MagicMock(
        return_value=embedded_documents
    )

    # ==========================================================
    # Build index
    # ==========================================================

    result = service.build_index(request)

    assert result == embedded_documents

    # Correct database-specific store should be selected
    service.get_index_store.assert_called_with(
        "northwind"
    )

    # Completed index should be persisted
    mock_store.save.assert_called_once_with(
        embedded_documents
    )

    # ==========================================================
    # Load index
    # ==========================================================

    mock_store.load.return_value = embedded_documents

    loaded = service.load_index(
        "northwind"
    )

    assert loaded == embedded_documents

    mock_store.load.assert_called_once_with()

    # ==========================================================
    # Verify indexing pipeline
    # ==========================================================

    service.database_service.get_schema.assert_called_once_with(
        request
    )

    service.knowledge_builder.build_database_knowledge.assert_called_once_with(
        schema
    )

    service.document_builder.build.assert_called_once_with(
        schema,
        knowledge
    )

    service.embedding_builder.build_embeddings.assert_called_once_with(
        documents
    )

    print("IndexingService test passed.")


if __name__ == "__main__":
    main()
    