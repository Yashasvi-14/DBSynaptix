from unittest.mock import MagicMock

from app.services.indexing_service import IndexingService


def main():

    service = IndexingService()

    service.index_store = MagicMock()

    request = MagicMock()

   
    # Fake pipeline data

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

    
    # Mock each indexing stage

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

    
    # Build index

    result = service.build_index(request)

    service.index_store.save.assert_called_once_with(
        embedded_documents
    )

    service.index_store.load.return_value = embedded_documents

    loaded = service.load_index()

    assert loaded == embedded_documents

    service.index_store.load.assert_called_once()

    assert result == embedded_documents

    
    # Verify pipeline order/data flow

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