from app.ai.provider import AIProvider
from app.sql.sql_validator import SQLValidator
from app.sql.sql_executor import SQLExecutor
from app.ai.retrieval import RetrievalEngine
from app.context.context_builder import ContextBuilder
from app.sql.prompt_builder import PromptBuilder
from app.sql.sql_repair import SQLRepair
from psycopg import Error as PsycopgError

class TextToSQLService:

    def __init__(self):

        self.ai = AIProvider()

        self.retriever = RetrievalEngine()

        self.context_builder = ContextBuilder()

        self.prompt_builder = PromptBuilder()

        self.validator = SQLValidator()

        self.executor = SQLExecutor()

        self.repairer = SQLRepair()

    def answer_question(
        self,
        question,
        request,
        documents
    ):
        # Retrieve relevant schema documents
        retrieved = self.retriever.retrieve(
            documents,
            question
        )

        # Expand retrieved context using database relationships
        context = self.context_builder.expand(
            retrieved,
            documents
        )

        # Build generation prompt
        prompt = self.prompt_builder.build(
            question,
            context
        )

        # Generate initial SQL
        llm_response = self.ai.generate_text_with_metadata(
            prompt
        )

        sql = self.validator.validate(
            llm_response.text
        )

        repair_attempted = False
        repair_successful = False

        try:
            # First execution attempt
            results = self.executor.execute(
                sql,
                request
            )

        except PsycopgError as execution_error:

            repair_attempted = True

            # Ask the LLM to repair the failed SQL using
            # the PostgreSQL error and the same schema context.
            repaired_response = self.ai.generate_text_with_metadata(
                self.repairer.build_prompt(
                    question=question,
                    failed_sql=sql,
                    error=execution_error,
                    documents=context
                )
            ) 

            repaired_sql = self.validator.validate(
                repaired_response.text
            )

            # Exactly one retry.
            # If this fails, the exception propagates normally.
            results = self.executor.execute(
                repaired_sql,
                request
            )

            sql = repaired_sql
            repair_successful = True

            # Include both LLM calls in token totals
            prompt_tokens = (
                llm_response.usage_metadata.prompt_token_count
                + repaired_response.usage_metadata.prompt_token_count
            )

            completion_tokens = (
                llm_response.usage_metadata.candidates_token_count
                + repaired_response.usage_metadata.candidates_token_count
            )

            total_tokens = (
                llm_response.usage_metadata.total_token_count
                + repaired_response.usage_metadata.total_token_count
            )

        else:
            prompt_tokens = (
                llm_response.usage_metadata.prompt_token_count
            )

            completion_tokens = (
                llm_response.usage_metadata.candidates_token_count
            )

            total_tokens = (
                llm_response.usage_metadata.total_token_count
            )

        return {
            "question": question,
            "sql": sql,
            "results": results,

            "repair_attempted": repair_attempted,
            "repair_successful": repair_successful,

            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens
        }