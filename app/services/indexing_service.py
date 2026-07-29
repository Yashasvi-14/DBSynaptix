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
        index_store = self.get_index_store(
            request.database
        )
        index_store.save(documents)

        return documents

    def load_index(
            self,
            database_name
        ):
        """
        Load the previously generated semantic index.
        """
        index_store = self.get_index_store(
            database_name
        )
        return index_store.load()

       
    def get_index_store(
        self,
        database_name
    ):
        """
        Return the persistent index store for a database.
        """

        return IndexStore(
            path=f"data/indexes/{database_name}.json"
        )