class PromptBuilder:

    def build(
        self,
        question,
        documents
    ):
        """
        Build the final prompt sent to the LLM.
        """

        lines = []

        # System Role
        lines.append(
            "You are an expert PostgreSQL database engineer."
        )

        lines.append(
            "Your job is to convert natural language questions into valid PostgreSQL SQL queries."
        )

        lines.append("")


        lines.append("IMPORTANT RULES")
        lines.append("------")

        lines.append(
            "1. Return ONLY SQL. Generate SQL that fully answers the user's question. If multiple entities are mentioned (e.g. customers and products), include information about all of them whenever appropriate."
        )

        lines.append(
            "2. Do NOT explain your reasoning."
        )

        lines.append(
            "3. Do NOT use markdown."
        )

        lines.append(
            "4. Do NOT wrap SQL inside ```."
        )

        lines.append(
            "5. Use ONLY tables and columns provided."
        )

        lines.append(
            "6. Never invent schema."
        )

        lines.append(
            "7. Generate PostgreSQL compatible SQL."
        )

        lines.append(
            "8. If the requested information cannot be answered using the provided schema, return exactly: SCHEMA_NOT_FOUND"
        )

        lines.append(
            "9. Prefer JOINs using the provided foreign key relationships."
        )

        lines.append(
            "10. Select only the columns required to answer the question."
        )

        lines.append("")

        
        # User Question
        

        lines.append("=" * 70)
        lines.append("USER QUESTION")
        lines.append("=" * 70)

        lines.append(question)

        lines.append("")

       
        # Retrieved Schema
        

        lines.append("=" * 70)
        lines.append("RETRIEVED DATABASE SCHEMA")
        lines.append("=" * 70)

        for document in documents:

            lines.append(document["text"])

            lines.append("")
            lines.append("-" * 70)
            lines.append("")

       
        # Output
        lines.append(
            "Generate ONLY the SQL query."
        )

        return "\n".join(lines)