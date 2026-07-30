from app.ai.retrieval import RetrievalEngine


def test_table_name_scoring():
    engine = RetrievalEngine()

    result = engine.score_table_name(
        "customers",
        ["customer", "delhi"],
    )

    assert result is not None


def test_column_scoring():
    engine = RetrievalEngine()

    columns = [
        {"name": "customer_id"},
        {"name": "total_amount"},
    ]

    result = engine.score_columns(
        columns,
        ["customer"],
    )

    assert result is not None


def test_document_scoring():
    engine = RetrievalEngine()

    document = {
        "table": "orders",
        "structured": {
            "columns": [
                {"name": "id"},
                {"name": "customer_id"},
                {"name": "total_amount"},
            ]
        },
    }

    result = engine.score_document(
        document,
        ["customer", "orders"],
        semantic_score=0.8,
    )

    assert result is not None