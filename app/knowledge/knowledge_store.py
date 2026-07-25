import json
from dataclasses import asdict

from app.knowledge.models import TableKnowledge


class KnowledgeStore:

    def __init__(self):

        self.tables = {}


    def add(
    self,
    knowledge: TableKnowledge
    ):
        """
        Add or replace table knowledge.
        """

        self.tables[
            knowledge.table
        ] = knowledge

    def get(
        self,
        table_name
    ):
        """
        Retrieve knowledge for one table.
        """

        return self.tables.get(table_name)
    
    def all(self):
        """
        Return every table.
        """

        return self.tables
    
    def save(
        self,
        filepath
    ):

        data = {}

        for table, knowledge in self.tables.items():

            data[table] = asdict(
                knowledge
            )

        with open(
            filepath,
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    def load(
        self,
        filepath
    ):

        with open(
            filepath,
            "r"
        ) as file:

            data = json.load(file)

        self.tables = {}

        for table, value in data.items():

            self.tables[table] = (
                TableKnowledge(
                    **value
                )
            )
    
    def exists(
        self,
        table_name
    ):
        return table_name in self.tables