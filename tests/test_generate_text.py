from app.ai.provider import AIProvider

provider = AIProvider()

response = provider.generate_text(
    """
Say hello in one sentence.
"""
)

print(response)