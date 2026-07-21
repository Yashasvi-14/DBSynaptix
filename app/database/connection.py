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


def get_columns(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            table_name,
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
    """)

    rows = cursor.fetchall()

    cursor.close()

    columns = {}

    for table_name, column_name, data_type in rows:

        if table_name not in columns:
            columns[table_name] = []

        columns[table_name].append({
            "name": column_name,
            "type": data_type
        })

    return columns

def get_primary_keys(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            tc.table_name,
            kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
        WHERE tc.constraint_type = 'PRIMARY KEY'
          AND tc.table_schema = 'public'
        ORDER BY tc.table_name;
    """)

    rows = cursor.fetchall()

    cursor.close()

    primary_keys = {}

    for table_name, column_name in rows:

        if table_name not in primary_keys:
            primary_keys[table_name] = []

        primary_keys[table_name].append(column_name)

    return primary_keys

def get_foreign_keys(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            tc.table_name,
            kcu.column_name,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage ccu
            ON tc.constraint_name = ccu.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY'
          AND tc.table_schema = 'public'
        ORDER BY tc.table_name;
    """)

    rows = cursor.fetchall()

    cursor.close()

    foreign_keys = {}

    for table_name, column_name, foreign_table_name, foreign_column_name in rows:

        if table_name not in foreign_keys:
            foreign_keys[table_name] = []

        foreign_keys[table_name].append(
            {
                "column": column_name,
                "references": {
                    "table": foreign_table_name,
                    "column": foreign_column_name
                }
            }
        )

    return foreign_keys


