from app.knowledge.knowledge_builder import KnowledgeBuilder

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

knowledge_store = builder.build_database_knowledge(schema)

for table_name, knowledge in knowledge_store.items():

    print("=" * 80)
    print(f"TABLE: {table_name}")
    print("=" * 80)

    print("\nSummary:")
    print(knowledge.summary)

    print("\nBusiness Terms:")
    print(knowledge.business_terms)

    print("\nColumn Descriptions:")
    for column, description in knowledge.column_descriptions.items():
        print(f"  {column}: {description}")

    print("\nSample Queries:")
    for query in knowledge.sample_queries:
        print(f"  - {query}")

    print("\n")