from fastapi import APIRouter

from app.schemas.query import QueryRequest, QueryResponse
from app.services.indexing_service import IndexingService
from app.services.text_to_sql_service import TextToSQLService


router = APIRouter(
    prefix="/query",
    tags=["Query"]
)


@router.post(
    "",
    response_model=QueryResponse
)
def query_database(
    request: QueryRequest
):
    """
    Convert a natural-language question into SQL
    and execute it against the connected database.
    """

    indexing_service = IndexingService()
    text_to_sql_service = TextToSQLService()

    # Load the persistent semantic index.
    documents = indexing_service.load_index(
        request.database.database
    )

    # Run the Text-to-SQL pipeline.
    result = text_to_sql_service.answer_question(
        question=request.question,
        request=request.database,
        documents=documents
    )

    return QueryResponse(**result)