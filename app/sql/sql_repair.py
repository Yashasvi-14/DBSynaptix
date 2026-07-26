from app.ai.provider import AIProvider


class SQLRepair:
    """
    Repairs SQL queries that fail during database execution.

    The repair process uses:
    - the original user question
    - the failed SQL query
    - the PostgreSQL error
    - the retrieved database schema
    """

    def __init__(self):
        self.ai = AIProvider()

    def repair(
        self,
        question,
        failed_sql,
        error,
        documents
    ):
        prompt = self.build_prompt(
            question,
            failed_sql,
            error,
            documents
        )

        return self.ai.generate_text(prompt)

    def build_prompt(
        self,
        question,
        failed_sql,
        error,
        documents
    ):
        lines = []

        # System role
        lines.append(
            "You are an expert PostgreSQL database engineer."
        )

        lines.append(
            "A previously generated SQL query failed during execution."
        )

        lines.append(
            "Your job is to repair the SQL query using the database error and provided schema."
        )

        lines.append("")

        # Rules
        lines.append("IMPORTANT RULES")
        lines.append("------")

        lines.append(
            "1. Return ONLY the corrected SQL query."
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
            "5. Use ONLY tables and columns provided in the schema."
        )

        lines.append(
            "6. Never invent tables or columns."
        )

        lines.append(
            "7. Generate PostgreSQL compatible SQL."
        )

        lines.append(
            "8. Preserve the intent of the original user question."
        )

        lines.append(
            "9. Use the database error to identify what was wrong with the failed query."
        )

        lines.append(
            "10. Prefer JOINs using the provided foreign key relationships."
        )

        lines.append(
            "11. If the question cannot be answered using the provided schema, return exactly: SCHEMA_NOT_FOUND"
        )

        lines.append("")

        # Original question
        lines.append("=" * 70)
        lines.append("ORIGINAL USER QUESTION")
        lines.append("=" * 70)

        lines.append(question)
        lines.append("")

        # Failed SQL
        lines.append("=" * 70)
        lines.append("FAILED SQL")
        lines.append("=" * 70)

        lines.append(failed_sql)
        lines.append("")

        # PostgreSQL error
        lines.append("=" * 70)
        lines.append("DATABASE ERROR")
        lines.append("=" * 70)

        lines.append(str(error))
        lines.append("")

        # Schema context
        lines.append("=" * 70)
        lines.append("RETRIEVED DATABASE SCHEMA")
        lines.append("=" * 70)

        for document in documents:
            lines.append(document["text"])
            lines.append("")
            lines.append("-" * 70)
            lines.append("")

        lines.append(
            "Generate ONLY the corrected SQL query."
        )

        return "\n".join(lines)