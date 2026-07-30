from unittest.mock import MagicMock

from app.indexing.embedding_builder import EmbeddingBuilder


def test_build_embeddings():
    builder = EmbeddingBuilder()

    # Replace the real AI provider so Gemini is never called.
    builder.provider = MagicMock()

    builder.provider.generate_embedding.side_effect = [
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
    ]

    documents = [
        {
            "table": "customers",
            "text": "TABLE: customers",
            "embedding": None,
        },
        {
            "table": "orders",
            "text": "TABLE: orders",
            "embedding": None,
        },
    ]

    result = builder.build_embeddings(documents)

    assert result[0]["embedding"] == [0.1, 0.2, 0.3]
    assert result[1]["embedding"] == [0.4, 0.5, 0.6]

    assert builder.provider.generate_embedding.call_count == 2

    builder.provider.generate_embedding.assert_any_call(
        "TABLE: customers"
    )

    builder.provider.generate_embedding.assert_any_call(
        "TABLE: orders"
    )


def test_existing_embedding_is_reused():
    builder = EmbeddingBuilder()

    builder.provider = MagicMock()

    documents = [
        {
            "table": "customers",
            "text": "TABLE: customers",
            "embedding": [0.1, 0.2, 0.3],
        }
    ]

    result = builder.build_embeddings(documents)

    assert result[0]["embedding"] == [0.1, 0.2, 0.3]

    builder.provider.generate_embedding.assert_not_called()