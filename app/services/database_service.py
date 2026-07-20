from app.database.connection import create_connection, get_tables
from app.schemas.database import DatabaseConnectionRequest
from app.schemas.response import ApiResponse

class DatabaseService:

    def connect(self, request: DatabaseConnectionRequest):

        connection = create_connection(request)

        connection.close()

        return ApiResponse(
            success=True,
            message="Database connection successful"
        )
    
    def get_schema(self, request: DatabaseConnectionRequest):

        connection = create_connection(request)

        try:
            tables = get_tables(connection)

            return ApiResponse(
                success=True,
                message="Schema retrieved successfully",
                data=tables
            )

        finally:
            connection.close()