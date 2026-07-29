from app.database.connection import (
    create_connection,
    get_primary_keys,
    get_foreign_keys
)
from app.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)

from app.schemas.database import DatabaseConnectionRequest


request = DatabaseConnectionRequest(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    username=DB_USER,
    password=DB_PASSWORD
)


connection = create_connection(request)


primary_keys = get_primary_keys(connection)

print(primary_keys)

connection.close()

connection = create_connection(request)

foreign_keys = get_foreign_keys(connection)

print(foreign_keys)

connection.close()