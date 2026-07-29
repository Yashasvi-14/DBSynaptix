from app.ai.provider import AIProvider
from app.sql.sql_executor import SQLExecutor
from app.sql.sql_validator import SQLValidator
from app.sql.sql_repair import SQLRepair
from app.schemas.database import DatabaseConnectionRequest
from psycopg import Error as PsycopgError
from app.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)

def main():

    ai = AIProvider()
    executor = SQLExecutor()
    validator = SQLValidator()
    repairer = SQLRepair()

    # Northwind database connection
    request = DatabaseConnectionRequest(
        host="localhost",
        port=5432,
        database="northwind",
        username="postgres",
        password=DB_PASSWORD
    )

    question = "List all customer contact names."

    # Intentionally incorrect column.
    failed_sql = """
SELECT customer_name
FROM customers;
"""

    # Minimal real schema context needed for repair.
    documents = [
        {
            "table": "customers",
            "text": """
TABLE: customers

COLUMNS:
- customer_id
- company_name
- contact_name
- contact_title
- address
- city
- region
- postal_code
- country
- phone
- fax
"""
        }
    ]

    print("=" * 80)
    print("INITIAL SQL")
    print("=" * 80)
    print(failed_sql)

    try:

        executor.execute(
            failed_sql,
            request
        )

        raise AssertionError(
            "Initial SQL was expected to fail."
        )

    except PsycopgError as execution_error:

        print("\nPostgreSQL error:")
        print(execution_error)

        repair_prompt = repairer.build_prompt(
            question=question,
            failed_sql=failed_sql,
            error=execution_error,
            documents=documents
        )

        response = ai.generate_text_with_metadata(
            repair_prompt
        )

        repaired_sql = validator.validate(
            response.text
        )

        print("\n" + "=" * 80)
        print("REPAIRED SQL")
        print("=" * 80)

        print(repaired_sql)

        results = executor.execute(
            repaired_sql,
            request
        )

        print("\n" + "=" * 80)
        print("EXECUTION SUCCESSFUL")
        print("=" * 80)

        print(f"Rows returned: {len(results)}")

        for row in results[:5]:
            print(row)

        print("\nToken usage:")
        print(
            "Prompt:",
            response.usage_metadata.prompt_token_count
        )
        print(
            "Completion:",
            response.usage_metadata.candidates_token_count
        )
        print(
            "Total:",
            response.usage_metadata.total_token_count
        )

        print("\nREAL SQL REPAIR TEST PASSED")


if __name__ == "__main__":
    main()