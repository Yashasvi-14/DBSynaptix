from app.knowledge.knowledge_builder import KnowledgeBuilder
from app.knowledge.knowledge_store import KnowledgeStore
from app.indexing.document_builder import DocumentBuilder
from app.indexing.embedding_builder import EmbeddingBuilder
from app.ai.retrieval import RetrievalEngine
from app.sql.prompt_builder import PromptBuilder

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


def build_documents():
    """
    Build the complete offline indexing pipeline.
    """

    # ----------------------------
    # Build Knowledge
    # ----------------------------

    knowledge_builder = KnowledgeBuilder()

    knowledge = knowledge_builder.build_database_knowledge(
        schema
    )

    # ----------------------------
    # Store Knowledge
    # ----------------------------

    store = KnowledgeStore()

    for table in knowledge.values():
        store.add(table)

    # ----------------------------
    # Build Documents
    # ----------------------------

    document_builder = DocumentBuilder()

    documents = document_builder.build(
        schema,
        store
    )

    # ----------------------------
    # Build Embeddings
    # ----------------------------

    embedding_builder = EmbeddingBuilder()

    documents = embedding_builder.build_embeddings(
        documents
    )

    return documents


def main():

    documents = build_documents()

    retrieval_engine = RetrievalEngine()

    prompt_builder = PromptBuilder()

    questions = [

        "Show customers from Delhi",

        "Highest revenue",

        "Products bought by customers",

        "Average order value",

        "Purchase history",

        "Top customers"
    ]

    for question in questions:

        print("\n")
        print("=" * 100)
        print(f"QUESTION : {question}")
        print("=" * 100)

        # ---------------------------------------
        # Retrieve top relevant documents
        # ---------------------------------------

        results = retrieval_engine.retrieve(
            documents,
            question
        )

        top_documents = []

        for result in results[:3]:

            top_documents.append(
                result["document"]
            )

        # ---------------------------------------
        # Build Prompt
        # ---------------------------------------

        prompt = prompt_builder.build(
            question,
            top_documents
        )

        print(prompt)

        print("=" * 100)


if __name__ == "__main__":
    main()