from app.ai.retrieval import RetrievalEngine

engine = RetrievalEngine()

print(
    engine.score_table_name(
        "customers",
        ["customer", "delhi"]
    )
)

print()

columns = [
    {
        "name": "customer_id"
    },
    {
        "name": "total_amount"
    }
]

print(
    engine.score_columns(
        columns,
        ["customer"]
    )
)

document = {

    "table": "orders",

    "structured": {

        "columns": [

            {"name":"id"},

            {"name":"customer_id"},

            {"name":"total_amount"}

        ]

    }
}

engine = RetrievalEngine()

result = engine.score_document(
    document,
    [
        "customer",
        "orders"
    ]
)

print(result)