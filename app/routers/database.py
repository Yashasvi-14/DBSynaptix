from fastapi import APIRouter
from app.schemas.database import DatabaseConnectionRequest
from app.services.database_service import DatabaseService
from app.services.indexing_service import IndexingService
from app.schemas.response import ApiResponse

router = APIRouter(
    prefix="/database",
    tags=["Database"]
)

@router.post("/connect")
def connect_database(request: DatabaseConnectionRequest):
    service = DatabaseService()
    return service.connect(request)

@router.post("/schema")
def get_database_schema(request: DatabaseConnectionRequest):
    service = DatabaseService()
    return service.get_schema(request)

@router.post("/index")
def index_database(
    request: DatabaseConnectionRequest
):
    """
    Build and persist the semantic index
    for the connected database.
    """

    indexing_service = IndexingService()

    documents = indexing_service.build_index(
        request
    )

    return ApiResponse(
        success=True,
        message="Database indexed successfully",
        data={
            "indexed_tables": len(documents)
        }
    )