from fastapi import APIRouter
from app.schemas.database import DatabaseConnectionRequest
from app.services.database_service import DatabaseService
from app.services.indexing_service import IndexingService
from app.schemas.response import ApiResponse
from fastapi import HTTPException
from psycopg import OperationalError

router = APIRouter(
    prefix="/database",
    tags=["Database"]
)

@router.post("/connect")
def connect_database(request: DatabaseConnectionRequest):
    service = DatabaseService()

    try:
        return service.connect(request)

    except OperationalError:
        raise HTTPException(
            status_code=400,
            detail="Unable to connect to database. Check your connection details."
        )

@router.post("/schema")
def get_database_schema(request: DatabaseConnectionRequest):
    service = DatabaseService()
    return service.get_schema(request)

@router.post("/index")
def index_database(
    request: DatabaseConnectionRequest
):
    indexing_service = IndexingService()

    if indexing_service.index_exists(
        request.database
    ):
        documents = indexing_service.load_index(
            request.database
        )

        return ApiResponse(
            success=True,
            message="Existing database index loaded",
            data={
                "indexed_tables": len(documents),
                "reused": True
            }
        )

    documents = indexing_service.build_index(
        request
    )

    return ApiResponse(
        success=True,
        message="Database indexed successfully",
        data={
            "indexed_tables": len(documents),
            "reused": False
        }
    )