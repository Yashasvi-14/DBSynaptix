from app.database.connection import create_connection, get_tables, get_columns, get_foreign_keys, get_primary_keys
from app.database.schema_builder import assemble_schema
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
            columns = get_columns(connection)

            primary_keys = get_primary_keys(connection)

            foreign_keys = get_foreign_keys(connection)

            schema = assemble_schema(
                columns,
                primary_keys,
                foreign_keys
            )


            return ApiResponse(
                success=True,
                message="Schema retrieved successfully",
                data=schema
            )

        finally:
            connection.close()