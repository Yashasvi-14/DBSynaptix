from app.ai.retrieval import RetrievalEngine
from app.context.context_builder import ContextBuilder
from app.indexing.document_builder import DocumentBuilder
from app.indexing.embedding_builder import EmbeddingBuilder
from app.knowledge.knowledge_builder import KnowledgeBuilder
from app.knowledge.knowledge_store import KnowledgeStore

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

# ------------------------------------
# Build Offline Index
# ------------------------------------

knowledge_builder = KnowledgeBuilder()

knowledge = knowledge_builder.build_database_knowledge(
    schema
)

store = KnowledgeStore()

for table in knowledge.values():
    store.add(table)

document_builder = DocumentBuilder()

documents = document_builder.build(
    schema,
    store
)

embedding_builder = EmbeddingBuilder()

documents = embedding_builder.build_embeddings(
    documents
)


# ------------------------------------
# Retrieve
# ------------------------------------

retrieval = RetrievalEngine()

question = "Products bought by customers"

results = retrieval.retrieve(
    documents,
    question
)

print("=" * 70)
print("Retrieved Tables")
print("=" * 70)

for result in results[:3]:

    print(result["table"])


# ------------------------------------
# Expand Context
# ------------------------------------

builder = ContextBuilder()

expanded = builder.expand(
    results,
    documents
)

print()

print("=" * 70)
print("Expanded Tables")
print("=" * 70)

for document in expanded:

    print(document["table"])