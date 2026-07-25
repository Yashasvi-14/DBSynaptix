from app.ai.similarity import SimilarityCalculator

calculator = SimilarityCalculator()

vector1 = [1,0]

vector2 = [1,1]

print(
    calculator.cosine_similarity(
        vector1,
        vector2
    )
)