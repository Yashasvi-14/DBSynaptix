import json

from app.ai.provider import AIProvider
from app.knowledge.models import TableKnowledge
from app.knowledge.prompts import build_knowledge_prompt


class KnowledgeBuilder:

    def __init__(self):

        self.provider = AIProvider()

    def build_table_knowledge(
        self,
        table_name,
        table_schema
    ) -> TableKnowledge:
        """
        Generate semantic knowledge for one table.
        """

        prompt = build_knowledge_prompt(
            table_name,
            table_schema
        )

        response = self.provider.generate_text(
            prompt
        )


        knowledge = json.loads(response)

        return TableKnowledge(

            table=table_name,

            summary=knowledge["summary"],

            business_terms=knowledge["business_terms"],

            column_descriptions=knowledge["column_descriptions"],

            sample_queries=knowledge["sample_queries"]

        )
    
    def build_database_knowledge(
        self,
        schema
    ):
        """
        Generate knowledge for the complete database.
        """

        knowledge_store = {}

        for table_name, table_schema in schema.items():

            print(f"Building knowledge for {table_name}...")

            knowledge_store[table_name] = (
                self.build_table_knowledge(
                    table_name,
                    table_schema
                )
            )

        return knowledge_store