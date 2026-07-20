import psycopg
from app.schemas.database import DatabaseConnectionRequest


def create_connection(request: DatabaseConnectionRequest):
    connection = psycopg.connect(
        host=request.host,
        port=request.port,
        dbname=request.database,
        user=request.username,
        password=request.password,
    )

    return connection
  
def get_tables(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)

    tables = [row[0] for row in cursor.fetchall()]

    cursor.close()

    return tables