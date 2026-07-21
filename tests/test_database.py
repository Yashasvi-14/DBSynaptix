from app.database.connection import (
    create_connection,
    get_primary_keys,
    get_foreign_keys
)

from app.schemas.database import DatabaseConnectionRequest


request = DatabaseConnectionRequest(
    host="localhost",
    port=5432,
    database="DB-BlackBox",
    username="postgres",
    password="Yash@1403"
)


connection = create_connection(request)


primary_keys = get_primary_keys(connection)

print(primary_keys)

connection.close()

connection = create_connection(request)

foreign_keys = get_foreign_keys(connection)

print(foreign_keys)

connection.close()