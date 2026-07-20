from fastapi import APIRouter
from app.schemas.database import DatabaseConnectionRequest
from app.services.database_service import DatabaseService

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