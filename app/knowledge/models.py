from dataclasses import dataclass


@dataclass
class TableKnowledge:
    """
    AI-generated semantic knowledge for one database table.
    """

    table: str

    summary: str

    business_terms: list[str]

    column_descriptions: dict[str, str]

    sample_queries: list[str]