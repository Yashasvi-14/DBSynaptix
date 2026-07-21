import re
import string

class ContextEngine:

    IGNORE_WORDS = {
        "show",
        "list",
        "display",
        "give",
        "get",
        "find",
        "all",
        "the",
        "a",
        "an",
        "is",
        "are",
        "of"
    }

    def extract_keywords(self, question: str):

        # Convert to lowercase
        question = question.lower()

        # Remove punctuation
        question = question.translate(
            str.maketrans("", "", string.punctuation)
        )

        # Normalize whitespace
        question = re.sub(r"\s+", " ", question).strip()

        # Split into words
        words = question.split()

        # Remove stop words
        keywords = [
            word
            for word in words
            if word not in self.IGNORE_WORDS
        ]

        return keywords