from app.knowledge.knowledge_builder import KnowledgeBuilder

schema = {

    "columns": [

        {
            "name": "customer_id",
            "type": "integer"
        },

        {
            "name": "order_date",
            "type": "date"
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

builder = KnowledgeBuilder()

builder.build_table_knowledge(
    "orders",
    schema
)