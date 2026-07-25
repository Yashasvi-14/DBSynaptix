from app.ai.provider import AIProvider
from app.ai.similarity import SimilarityCalculator

provider = AIProvider()

embedding1 = provider.generate_embedding(
"""
Table: customers

Columns:
- id
- name
- city
- email

Primary Keys:
- id
"""
)

embedding2 = provider.generate_embedding(
"""
Information about buyers including their names,
cities and email addresses.
"""
)

calculator = SimilarityCalculator()

print(
    calculator.cosine_similarity(
        embedding1,
        embedding2
    )
)