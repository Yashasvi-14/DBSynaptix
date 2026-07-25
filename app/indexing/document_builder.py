class DocumentBuilder:
    """
    Builds retrieval documents from the database schema and
    generates embeddings for semantic search.
    """

    COLUMN_DESCRIPTIONS = {
        "id": "Unique identifier.",
        "name": "Stores the name.",
        "email": "Stores the email address.",
        "city": "Stores the city.",
        "price": "Stores the price.",
        "amount": "Stores a monetary amount.",
        "date": "Stores a date."
    }

    def build(self, schema, knowledge_store):
        """
        Convert the complete schema into retrieval documents.
        """

        documents = []

        for table_name, table_schema in schema.items():
            knowledge = knowledge_store.get(table_name)
            document = self.build_table_document(
                table_name,
                table_schema,
                knowledge
            )

            documents.append(document)

        return documents

    def build_table_document(self, table_name, table_schema, knowledge):
        """
        Build one retrieval document for a table.
        """

        lines = []

        # Table
        lines.append("=" * 60)
        lines.append(f"TABLE: {table_name.upper()}")
        lines.append("=" * 60)
        lines.append("")
        lines.append("SUMMARY")
        lines.append("")

        lines.append(
            knowledge.summary
        )
        lines.append("")
        lines.append("BUSINESS TERMS")
        lines.append("")

        for term in knowledge.business_terms:

            lines.append(
                f"- {term}"
            )

        lines.append("")

        # Columns
        lines.append("Columns:")

        for column in table_schema["columns"]:

            lines.append(
                f"- {column['name']} ({column['type']})"
            )

            description = (
                knowledge.column_descriptions.get(
                column["name"],
                ""
                )  
            )

            if description:
                lines.append(f"  {description}")

        lines.append("")

        # Primary Keys
        lines.append("Primary Keys:")

        if table_schema["primary_keys"]:

            for key in table_schema["primary_keys"]:

                lines.append(f"- {key}")

        else:

            lines.append("None")

        lines.append("")

        
        # Relationships
        lines.append("FOREIGN KEYS:")

        if table_schema["foreign_keys"]:

            for fk in table_schema["foreign_keys"]:

                lines.append(
                    self.describe_foreign_key(fk)
                )

        else:

            lines.append("None")

        lines.append("")

        lines.append(
            "EXAMPLE QUESTIONS"
        )

        lines.append("")
        for query in knowledge.sample_queries:

            lines.append(
                f"- {query}"
            )
        
        text = "\n".join(lines)
        return {
            "table": table_name,
            "structured": table_schema,
            "text": text,
            "embedding": None
        }

    def describe_foreign_key(self, fk):
        """
        Generate a natural-language description
        for a foreign key.
        """

        column = fk["column"]

        reference_table = fk["references"]["table"]

        reference_column = fk["references"]["column"]

        return (
            f"- {column} references "
            f"{reference_table}.{reference_column}."
        )