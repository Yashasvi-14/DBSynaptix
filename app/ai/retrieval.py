from app.ai.preprocessing import QueryPreprocessor
from app.ai.provider import AIProvider
from app.ai.similarity import SimilarityCalculator


class RetrievalEngine:

    TABLE_MATCH_SCORE = 10
    COLUMN_MATCH_SCORE = 5

    KEYWORD_WEIGHT = 0.4
    SEMANTIC_WEIGHT = 0.6

    def __init__(self):

        self.preprocessor = QueryPreprocessor()
        self.provider = AIProvider()
        self.similarity = SimilarityCalculator()

    # Keyword Scoring

    def score_table_name(self, table_name, keywords):
        """
        Score a table name based on keyword matches.
        """

        score = 0
        matches = []

        table_name = table_name.lower()

        for keyword in keywords:

            keyword = keyword.lower()

            if keyword in table_name:
                score += self.TABLE_MATCH_SCORE
                matches.append(keyword)
        
        max_score = len(keywords) * self.TABLE_MATCH_SCORE
        normalized_score = 0
        if max_score != 0:
            normalized_score = score/max_score
        return {
            "raw_score": score,
            "normalized_score": normalized_score,
            "matches": matches
        }

    def score_columns(self, columns, keywords):
        """
        Score columns based on keyword matches.
        Returns:
        {
            "raw_score": float,
            "normalized_score": float,
            "matches": list
        }
        """

        score = 0
        matches = []

        for keyword in keywords:

            keyword = keyword.lower()

            for column in columns:

                column_name = column["name"].lower()

                if keyword in column_name:

                    score += self.COLUMN_MATCH_SCORE
                    matches.append(column["name"])

                    # Prevent one keyword from scoring multiple columns
                    break

        max_score = len(keywords) * self.COLUMN_MATCH_SCORE

        normalized_score = 0

        if max_score != 0:
            normalized_score = score / max_score

        return {
            "raw_score": score,
            "normalized_score": normalized_score,
            "matches": matches
        }

    # Semantic Scoring
    
    def score_semantic(
        self,
        document,
        question_embedding
    ):
        """
        Calculate semantic similarity between the
        question embedding and document embedding.
        """

        return self.similarity.cosine_similarity(
            question_embedding,
            document["embedding"]
        )

    
    # Hybrid Scoring

    def score_document(
        self,
        document,
        keywords,
        semantic_score
    ):
        """
        Combine keyword score and semantic score.
        """

        table_result = self.score_table_name(
            document["table"],
            keywords
        )

        column_result = self.score_columns(
            document["structured"]["columns"],
            keywords
        )

        keyword_score = (
            table_result["normalized_score"] +
            column_result["normalized_score"]
        ) / 2

        final_score = (
            self.KEYWORD_WEIGHT * keyword_score +
            self.SEMANTIC_WEIGHT * semantic_score
        )

        return {

            "table": document["table"],

            "keyword_score": keyword_score,

            "semantic_score": semantic_score,

            "final_score": final_score,

            "reasons": {

                "table_matches": table_result["matches"],
                "column_matches": column_result["matches"],
                "raw_table_score": table_result["raw_score"],
                "raw_column_score": column_result["raw_score"]

            },

            "document": document
        }

    # Main Retrieval Pipeline

    def retrieve(
        self,
        documents,
        question
    ):
        """
        Retrieve and rank documents based on
        keyword + semantic similarity.
        """

        processed_query = self.preprocessor.preprocess(question)

        keywords = processed_query["keywords"]

        # Generate question embedding only once
        question_embedding = self.provider.generate_embedding(
            question
        )

        scored_documents = []

        for document in documents:

            semantic_score = self.score_semantic(
                document,
                question_embedding
            )

            result = self.score_document(
                document,
                keywords,
                semantic_score
            )

            if result["final_score"] > 0:
                scored_documents.append(result)

        scored_documents.sort(
            key=lambda doc: doc["final_score"],
            reverse=True
        )

        return scored_documents