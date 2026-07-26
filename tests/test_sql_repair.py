from app.sql.sql_repair import SQLRepair
from unittest.mock import MagicMock

from app.services.text_to_sql_service import TextToSQLService
from psycopg import Error as PsycopgError

def test_repair_stops_after_one_attempt():

    service = TextToSQLService()

    documents = [
        {
            "table": "customers",
            "text": """
TABLE: customers

COLUMNS:
- customer_id
- company_name
- contact_name
""",
            "structured": {
                "foreign_keys": []
            }
        }
    ]

    service.retriever.retrieve = MagicMock(
        return_value=[
            {
                "table": "customers",
                "document": documents[0]
            }
        ]
    )

    service.context_builder.expand = MagicMock(
        return_value=documents
    )

    # Initial generation
    initial_response = MagicMock()
    initial_response.text = (
        "SELECT customer_name FROM customers;"
    )

    initial_response.usage_metadata.prompt_token_count = 100
    initial_response.usage_metadata.candidates_token_count = 20
    initial_response.usage_metadata.total_token_count = 120

    # Repair generation
    repaired_response = MagicMock()
    repaired_response.text = (
        "SELECT full_name FROM customers;"
    )

    repaired_response.usage_metadata.prompt_token_count = 150
    repaired_response.usage_metadata.candidates_token_count = 25
    repaired_response.usage_metadata.total_token_count = 175

    service.ai.generate_text_with_metadata = MagicMock(
        side_effect=[
            initial_response,
            repaired_response
        ]
    )

    # Both execution attempts fail
    service.executor.execute = MagicMock(
        side_effect=[
            PsycopgError(
                'column "customer_name" does not exist'
            ),
            PsycopgError(
                'column "full_name" does not exist'
            )
        ]
    )

    request = MagicMock()

    try:

        service.answer_question(
            question="List all customer names.",
            request=request,
            documents=documents
        )

        # We should never reach here
        assert False, "Expected repaired execution to fail"

    except Exception as error:

        assert "full_name" in str(error)

    # Initial generation + ONE repair generation
    assert (
        service.ai.generate_text_with_metadata.call_count
        == 2
    )

    # Initial execution + ONE repaired execution
    assert service.executor.execute.call_count == 2

    print("SQL repair retry-limit test passed.")

def test_no_repair_when_execution_succeeds():

    service = TextToSQLService()

    documents = [
        {
            "table": "customers",
            "text": """
TABLE: customers

COLUMNS:
- customer_id
- company_name
- contact_name
""",
            "structured": {
                "foreign_keys": []
            }
        }
    ]

    service.retriever.retrieve = MagicMock(
        return_value=[
            {
                "table": "customers",
                "document": documents[0]
            }
        ]
    )

    service.context_builder.expand = MagicMock(
        return_value=documents
    )

    initial_response = MagicMock()

    initial_response.text = (
        "SELECT contact_name FROM customers;"
    )

    initial_response.usage_metadata.prompt_token_count = 100
    initial_response.usage_metadata.candidates_token_count = 20
    initial_response.usage_metadata.total_token_count = 120

    service.ai.generate_text_with_metadata = MagicMock(
        return_value=initial_response
    )

    service.executor.execute = MagicMock(
        return_value=[
            {
                "contact_name": "Maria Anders"
            }
        ]
    )

    request = MagicMock()

    result = service.answer_question(
        question="List all customer names.",
        request=request,
        documents=documents
    )

    assert result["repair_attempted"] is False
    assert result["repair_successful"] is False

    assert result["sql"] == (
        "SELECT contact_name FROM customers;"
    )

    assert result["results"] == [
        {
            "contact_name": "Maria Anders"
        }
    ]

    assert result["prompt_tokens"] == 100
    assert result["completion_tokens"] == 20
    assert result["total_tokens"] == 120

    # Only initial generation
    assert (
        service.ai.generate_text_with_metadata.call_count
        == 1
    )

    # Only initial execution
    assert service.executor.execute.call_count == 1

    print("SQL no-repair success test passed.")

def test_application_error_does_not_trigger_repair():

    service = TextToSQLService()

    documents = [
        {
            "table": "customers",
            "text": """
TABLE: customers

COLUMNS:
- customer_id
- company_name
- contact_name
""",
            "structured": {
                "foreign_keys": []
            }
        }
    ]

    service.retriever.retrieve = MagicMock(
        return_value=[
            {
                "table": "customers",
                "document": documents[0]
            }
        ]
    )

    service.context_builder.expand = MagicMock(
        return_value=documents
    )

    initial_response = MagicMock()

    initial_response.text = (
        "SELECT contact_name FROM customers;"
    )

    initial_response.usage_metadata.prompt_token_count = 100
    initial_response.usage_metadata.candidates_token_count = 20
    initial_response.usage_metadata.total_token_count = 120

    service.ai.generate_text_with_metadata = MagicMock(
        return_value=initial_response
    )

    # Simulate an application/programming error,
    # NOT a PostgreSQL error.
    service.executor.execute = MagicMock(
        side_effect=RuntimeError(
            "Unexpected application error"
        )
    )

    request = MagicMock()

    try:

        service.answer_question(
            question="List all customer names.",
            request=request,
            documents=documents
        )

        assert False, "Expected RuntimeError"

    except RuntimeError as error:

        assert "Unexpected application error" in str(error)

    # Critical assertion:
    # Gemini should only have been called for initial generation.
    assert (
        service.ai.generate_text_with_metadata.call_count
        == 1
    )

    # No retry should occur.
    assert service.executor.execute.call_count == 1

    print("Non-SQL error bypasses repair test passed.")

def main():

    repair = SQLRepair()

    documents = [
        {
            "table": "customers",
            "text": """
TABLE: customers

COLUMNS:
- customer_id
- company_name
- contact_name
- country
"""
        }
    ]

    question = "List all customer names."

    failed_sql = """
SELECT customer_name
FROM customers;
"""

    error = 'column "customer_name" does not exist'

    prompt = repair.build_prompt(
        question=question,
        failed_sql=failed_sql,
        error=error,
        documents=documents
    )

    print("=" * 80)
    print("SQL REPAIR PROMPT")
    print("=" * 80)

    print(prompt)

    print("=" * 80)

    # Verify important repair information exists
    assert question in prompt
    assert "SELECT customer_name" in prompt
    assert 'column "customer_name" does not exist' in prompt
    assert "customer_id" in prompt
    assert "company_name" in prompt
    assert "contact_name" in prompt

    print("SQL repair prompt test passed.")
    # Test complete self-correction flow
    test_repair_flow()
    test_repair_stops_after_one_attempt()
    test_no_repair_when_execution_succeeds()
    test_application_error_does_not_trigger_repair()



def test_repair_flow():

    service = TextToSQLService()

    # Fake schema documents
    documents = [
        {
            "table": "customers",
            "text": """
TABLE: customers

COLUMNS:
- customer_id
- company_name
- contact_name
- country
""",
            "structured": {
                "foreign_keys": []
            }
        }
    ]

    # Mock retrieval

    service.retriever.retrieve = MagicMock(
        return_value=[
            {
                "table": "customers",
                "document": documents[0]
            }
        ]
    )

    service.context_builder.expand = MagicMock(
        return_value=documents
    )

    # Mock initial LLM response

    initial_response = MagicMock()

    initial_response.text = (
        "SELECT customer_name FROM customers;"
    )

    initial_response.usage_metadata.prompt_token_count = 100
    initial_response.usage_metadata.candidates_token_count = 20
    initial_response.usage_metadata.total_token_count = 120

    # Mock repaired LLM response

    repaired_response = MagicMock()

    repaired_response.text = (
        "SELECT contact_name FROM customers;"
    )

    repaired_response.usage_metadata.prompt_token_count = 150
    repaired_response.usage_metadata.candidates_token_count = 25
    repaired_response.usage_metadata.total_token_count = 175

    service.ai.generate_text_with_metadata = MagicMock(
        side_effect=[
            initial_response,
            repaired_response
        ]
    )

    
    # First execution fails.
    # Second execution succeeds.
    

    service.executor.execute = MagicMock(
        side_effect=[
            PsycopgError(
                'column "customer_name" does not exist'
            ),
            [
                {
                    "contact_name": "Maria Anders"
                }
            ]
        ]
    )

    request = MagicMock()

    result = service.answer_question(
        question="List all customer names.",
        request=request,
        documents=documents
    )

    
    # Verify repair behaviour

    assert result["repair_attempted"] is True
    assert result["repair_successful"] is True

    assert result["sql"] == (
        "SELECT contact_name FROM customers;"
    )

    assert result["results"] == [
        {
            "contact_name": "Maria Anders"
        }
    ]

    # Both LLM calls should be counted.
    assert result["prompt_tokens"] == 250
    assert result["completion_tokens"] == 45
    assert result["total_tokens"] == 295

    # Generation + repair = exactly two LLM calls.
    assert (
        service.ai.generate_text_with_metadata.call_count
        == 2
    )

    # Initial execution + one repaired execution.
    assert service.executor.execute.call_count == 2

    print("SQL repair flow test passed.")



if __name__ == "__main__":
    main()

