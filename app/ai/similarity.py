import math


class SimilarityCalculator:

    def cosine_similarity(self, vector1, vector2):
        """
        Compute cosine similarity between two vectors.
        """

        dot = self.dot_product(
            vector1,
            vector2
        )

        magnitude1 = self.magnitude(vector1)

        magnitude2 = self.magnitude(vector2)

        if magnitude1 == 0 or magnitude2 == 0:
            return 0

        return dot / (magnitude1 * magnitude2)
    
    

    def dot_product(self, vector1, vector2):
        """
        Compute the dot product of two vectors.
       """

        result = 0

        for a, b in zip(vector1, vector2):
            result += a * b

        return result

    def magnitude(self, vector):
        """
        Compute vector magnitude.
        """

        total = 0

        for value in vector:
            total += value * value

        return math.sqrt(total)