from app.knowledge.knowledge_builder import KnowledgeBuilder
from app.knowledge.knowledge_store import KnowledgeStore
from app.indexing.document_builder import DocumentBuilder

schema = {

    "customers": {

        "columns": [
            {
                "name": "id",
                "type": "integer"
            },
            {
                "name": "name",
                "type": "varchar"
            },
            {
                "name": "email",
                "type": "varchar"
            },
            {
                "name": "city",
                "type": "varchar"
            }
        ],

        "primary_keys": [
            "id"
        ],

        "foreign_keys": []
    },

    "orders": {

        "columns": [
            {
                "name": "id",
                "type": "integer"
            },
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
            "id"
        ],

        "foreign_keys": [
            {
                "column": "customer_id",
                "references": {
                    "table": "customers",
                    "column": "id"
                }
            }
        ]
    },

    "products": {

        "columns": [
            {
                "name": "id",
                "type": "integer"
            },
            {
                "name": "name",
                "type": "varchar"
            },
            {
                "name": "category",
                "type": "varchar"
            },
            {
                "name": "price",
                "type": "numeric"
            }
        ],

        "primary_keys": [
            "id"
        ],

        "foreign_keys": []
    },

    "order_items": {

        "columns": [
            {
                "name": "id",
                "type": "integer"
            },
            {
                "name": "order_id",
                "type": "integer"
            },
            {
                "name": "product_id",
                "type": "integer"
            },
            {
                "name": "quantity",
                "type": "integer"
            }
        ],

        "primary_keys": [
            "id"
        ],

        "foreign_keys": [
            {
                "column": "order_id",
                "references": {
                    "table": "orders",
                    "column": "id"
                }
            },
            {
                "column": "product_id",
                "references": {
                    "table": "products",
                    "column": "id"
                }
            }
        ]
    }

}
builder = KnowledgeBuilder()

knowledge = builder.build_database_knowledge(schema)

store = KnowledgeStore()

for table in knowledge.values():
    store.add(table)

document_builder = DocumentBuilder()

documents = document_builder.build(
    schema,
    store
)

for document in documents:

    print("=" * 80)
    print(document["table"])
    print("=" * 80)

    print(document["text"])
    print()