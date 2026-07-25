from app.sql.sql_executor import SQLExecutor
from app.schemas.database import DatabaseConnectionRequest


def main():

    request = DatabaseConnectionRequest(
        host="localhost",
        port=5432,
        database="DB-BlackBox",
        username="postgres",
        password="Yash@1403"
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