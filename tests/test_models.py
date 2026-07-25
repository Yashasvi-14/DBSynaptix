from app.knowledge.models import TableKnowledge


knowledge = TableKnowledge(
    table="orders",

    summary="Stores customer purchase records.",

    business_terms=[
        "purchase",
        "sale",
        "transaction"
    ],

    column_descriptions={
        "customer_id": "Customer who placed the order.",
        "total_amount": "Total amount of the order."
    }
)

print(knowledge)