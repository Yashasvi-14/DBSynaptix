from app.knowledge.prompts import build_knowledge_prompt

schema = {
    "columns": [
        {
            "name": "customer_id",
            "type": "integer"
        },
        {
            "name": "total_amount",
            "type": "numeric"
        }
    ],

    "primary_keys": [
        "customer_id"
    ],

    "foreign_keys": []
}

prompt = build_knowledge_prompt(
    "orders",
    schema
)

print(prompt)