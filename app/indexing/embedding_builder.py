from app.ai.provider import AIProvider


class EmbeddingBuilder:
    """
    Generates embeddings for retrieval documents.
    """

    def __init__(self):

        self.provider = AIProvider()

    def build_embeddings(self, documents):
        """
        Generate embeddings for every retrieval document.

        Parameters
        ----------
        documents : list
            List of retrieval documents.

        Returns
        -------
        list
            Documents with embeddings populated.
        """

        for document in documents:

            if document["embedding"] is not None:
                continue

            document["embedding"] = self.provider.generate_embedding(
                document["text"]
            )

        return documents