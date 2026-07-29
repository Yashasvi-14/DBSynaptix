from app.sql.sql_executor import SQLExecutor
from app.schemas.database import DatabaseConnectionRequest
from app.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)

def main():

    request = DatabaseConnectionRequest(
        host="DB_HOST",
        port=DB_PORT,
        database=DB_NAME,
        username=DB_USER,
        password=DB_PASSWORD
    )

    sql = """
    SELECT
        SUM(total_amount) AS total_revenue
    FROM orders;
    """

    executor = SQLExecutor()

    results = executor.execute(
        sql,
        request
    )

    print("=" * 80)
    print("RESULT")
    print("=" * 80)

    for row in results:
        print(row)


if __name__ == "__main__":
    main()