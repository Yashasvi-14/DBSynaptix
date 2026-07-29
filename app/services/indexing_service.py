from app.services.database_service import DatabaseService

from app.knowledge.knowledge_builder import KnowledgeBuilder

from app.indexing.document_builder import DocumentBuilder
from app.indexing.embedding_builder import EmbeddingBuilder
from app.indexing.index_store import IndexStore

class IndexingService:
    """
    Builds the semantic index for a connected database.

    Pipeline:

    Database
        ↓
    Schema Extraction
        ↓
    Knowledge Generation
        ↓
    Document Building
        ↓
    Embedding Generation
    """

    def __init__(self):

        self.database_service = DatabaseService()

        self.knowledge_builder = KnowledgeBuilder()

        self.document_builder = DocumentBuilder()

        self.embedding_builder = EmbeddingBuilder()

        self.index_store = IndexStore()

    def build_index(
        self,
        request
    ):
        """
        Build the complete semantic index for a database.
        """

        # Extract database schema
        schema = self.database_service.get_schema(
            request
        ).data

        # Generate semantic knowledge
        knowledge = (
            self.knowledge_builder
            .build_database_knowledge(schema)
        )

        # Build retrieval documents
        documents = self.document_builder.build(
            schema,
            knowledge
        )

        # Generate embeddings
        documents = (
            self.embedding_builder
            .build_embeddings(documents)
        )

        # Persist the completed index
        self.index_store.save(documents)

        return documents

    def load_index(self):
        """
        Load the previously generated semantic index.
        """

        return self.index_store.load()