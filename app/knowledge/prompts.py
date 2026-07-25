import json


def build_knowledge_prompt(
    table_name,
    table_schema
):
    """
    Build the prompt used to generate semantic knowledge
    for a database table.
    """

    schema = json.dumps(
        table_schema,
        indent=4
    )

    prompt = f"""
You are an expert database architect.

Your task is to understand a database table and generate
structured semantic knowledge.

Table Name:
{table_name}

Schema:
{schema}

Generate ONLY valid JSON.

Return this exact format:

{{
    "summary": "...",

    "business_terms": [
        "...",
        "..."
    ],

    "column_descriptions": {{
        "column_name": "..."
    }},

    "sample_queries": [
        "...",
        "..."
    ]
}}

Rules:

1. summary should describe the business purpose of the table.

2. business_terms should contain common business words
related to the table. Return individual business terms. Do not return phrases. Each term should be one word whenever possible. Return only domain/business concepts that uniquely identify the table. Avoid generic database terms or concepts belonging to related tables.

3. column_descriptions should explain every important column.

4. sample_queries should contain natural language questions
that an end user would ask. Do NOT generate SQL.

Examples:

- Show total revenue.
- Find recent orders.
- List customer purchases.

Return JSON only.

Do NOT include markdown.

Do NOT explain your answer.
"""

    return prompt