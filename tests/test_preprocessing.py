from app.ai.preprocessing import QueryPreprocessor

processor = QueryPreprocessor()

result = processor.preprocess(
    "Show TOP!! 5 customers, by revenue in Delhi..."
)

print(result)