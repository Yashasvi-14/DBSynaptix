from app.ai.provider import AIProvider
from app.sql.sql_validator import SQLValidator
from app.sql.sql_executor import SQLExecutor
from app.ai.retrieval import RetrievalEngine
from app.context.context_builder import ContextBuilder
from app.sql.prompt_builder import PromptBuilder


class TextToSQLService:

    def __init__(self):

        self.ai = AIProvider()

        self.retriever = RetrievalEngine()

        self.context_builder = ContextBuilder()

        self.prompt_builder = PromptBuilder()

        self.validator = SQLValidator()

        self.executor = SQLExecutor()

    def answer_question(
        self,
        question,
        request,
        documents
    ):
        retrieved = self.retriever.retrieve(
            documents,
            question
        )

        context = self.context_builder.expand(
            retrieved,
            documents
        )

        prompt = self.prompt_builder.build(
            question,
            context
        )

        llm_response = self.ai.generate_text_with_metadata(prompt)

        sql = self.validator.validate(
            llm_response.text
        )

        results = self.executor.execute(
            sql,
            request
        )

        return {

            "question": question,

            "sql": sql,

            "results": results,

            "prompt_tokens": llm_response.usage_metadata.prompt_token_count,

            "completion_tokens": llm_response.usage_metadata.candidates_token_count,

            "total_tokens": llm_response.usage_metadata.total_token_count
        }