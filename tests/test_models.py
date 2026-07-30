from app.knowledge.models import TableKnowledge


def test_table_knowledge():
    knowledge = TableKnowledge(
        table="orders",
        summary="Stores customer purchase records.",
        business_terms=[
            "purchase",
            "sale",
            "transaction",
        ],
        column_descriptions={
            "customer_id": "Customer who placed the order.",
            "total_amount": "Total amount of the order.",
        },
        sample_queries=[
            "Show all orders",
            "Show orders for a customer",
        ],
    )

    assert knowledge.table == "orders"
    assert knowledge.summary == "Stores customer purchase records."
    assert "purchase" in knowledge.business_terms
    assert knowledge.column_descriptions["customer_id"] == (
        "Customer who placed the order."
    )
    assert len(knowledge.sample_queries) == 2