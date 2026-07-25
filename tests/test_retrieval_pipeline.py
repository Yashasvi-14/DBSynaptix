from app.ai.retrieval import RetrievalEngine
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

def build_pipeline():
    """
    Build the complete offline indexing pipeline.
    """

    print("=" * 80)
    print("BUILDING OFFLINE INDEX")
    print("=" * 80)

    # -------------------------------------------------
    # Build Knowledge
    # -------------------------------------------------

    knowledge_builder = KnowledgeBuilder()

    knowledge = knowledge_builder.build_database_knowledge(
        schema
    )

    # -------------------------------------------------
    # Store Knowledge
    # -------------------------------------------------

    store = KnowledgeStore()

    for table in knowledge.values():
        store.add(table)

    # -------------------------------------------------
    # Build Documents
    # -------------------------------------------------

    document_builder = DocumentBuilder()

    documents = document_builder.build(
        schema,
        store
    )

    # -------------------------------------------------
    # Build Embeddings
    # -------------------------------------------------

    embedding_builder = EmbeddingBuilder()

    documents = embedding_builder.build_embeddings(
        documents
    )

    print("\nOffline index built successfully.\n")

    return documents


def benchmark():
    """
    Benchmark retrieval quality.
    """

    documents = build_pipeline()

    retrieval_engine = RetrievalEngine()

    questions = [

        # Exact table names
        "show customers",
        "list products",
        "customer orders",

        # Semantic queries
        "buyers from delhi",
        "people living in delhi",
        "highest revenue",
        "sales this month",
        "purchase history",
        "money spent by customers",

        # Product synonyms
        "inventory",
        "merchandise",
        "expensive items",

        # Relationship queries
        "products bought by customers",
        "items in an order",

        # Aggregate queries
        "average order value",
        "top customers"
    ]

    print("=" * 100)
    print("RETRIEVAL BENCHMARK")
    print("=" * 100)

    for question in questions:

        print()
        print("=" * 100)
        print(f"QUESTION : {question}")
        print("=" * 100)

        results = retrieval_engine.retrieve(
            documents,
            question
        )

        if not results:
            print("No documents retrieved.")
            continue

        top_results = results[:3]

        margin = None

        if len(top_results) >= 2:
            margin = (
                top_results[0]["final_score"]
                - top_results[1]["final_score"]
            )

        for rank, result in enumerate(top_results, start=1):

            print()

            print(f"Rank #{rank}")

            print(
                f"Table           : {result['table']}"
            )

            print(
                f"Keyword Score   : "
                f"{result['keyword_score']:.3f}"
            )

            print(
                f"Semantic Score  : "
                f"{result['semantic_score']:.3f}"
            )

            print(
                f"Final Score     : "
                f"{result['final_score']:.3f}"
            )

            if rank == 1 and margin is not None:

                print(
                    f"Margin to Rank2 : "
                    f"{margin:.3f}"
                )

            print()

            print("Reasons")

            print(
                "Table Matches   :",
                result["reasons"]["table_matches"]
            )

            print(
                "Column Matches  :",
                result["reasons"]["column_matches"]
            )

            print(
                "Raw Table Score :",
                result["reasons"]["raw_table_score"]
            )

            print(
                "Raw Column Score:",
                result["reasons"]["raw_column_score"]
            )

    print()
    print("=" * 100)
    print("BENCHMARK COMPLETED")
    print("=" * 100)


if __name__ == "__main__":
    benchmark()