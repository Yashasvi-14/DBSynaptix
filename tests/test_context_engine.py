from app.ai.context_engine import ContextEngine

engine = ContextEngine()

result = engine.extract_keywords(
    "Show all customers from Delhi!!"
)

print(result)