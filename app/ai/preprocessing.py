import re


class QueryPreprocessor:

    def preprocess(self, question):
        """
        Main entry point.
        """

        normalized = self.normalize(question)

        tokens = self.tokenize(normalized)
        tokens = self.singularize(tokens)

        keywords = self.extract_keywords(tokens)

        return {
            "original": question,
            "normalized": normalized,
            "tokens": tokens,
            "keywords": keywords
        }

    def normalize(self, question):
        """
        Lowercase
        Remove punctuation
        Normalize whitespace
        """

        question = question.lower()

        # Remove punctuation
        question = re.sub(r"[^\w\s]", "", question)

        # Replace multiple spaces with one
        question = re.sub(r"\s+", " ", question)

        return question.strip()

    def tokenize(self, normalized_question):
        """
        Convert sentence into words.
        """

        return normalized_question.split()

    def extract_keywords(self, tokens):
        """
        Remove duplicate words while preserving order.
        """

        keywords = []
        seen = set()

        for token in tokens:

            if token not in seen:
                keywords.append(token)
                seen.add(token)

        return keywords
    
    def singularize(self, tokens):
        """
        Convert simple plural words into singular.
        """

        normalized = []

        for token in tokens:

            if token.endswith("ies"):

                token = token[:-3] + "y"

            elif token.endswith("s") and len(token) > 3:

                token = token[:-1]

            normalized.append(token)

        return normalized