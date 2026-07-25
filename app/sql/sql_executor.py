from app.services.database_service import DatabaseService


class SQLExecutor:
    """
    Executes validated SQL on PostgreSQL.
    """

    def __init__(self):

        self.database = DatabaseService()

    def execute(
        self,
        sql,
        request
    ):
        connection = self.database.get_connection(request)
        cursor = connection.cursor()
        try:

            cursor.execute(sql)

            rows = cursor.fetchall()

            column_names = [
                column[0]
                for column in cursor.description
            ]

            results = []

            for row in rows:

                results.append(
                    dict(
                        zip(
                            column_names,
                            row
                        )
                    )
                )

            return results

        finally:

            cursor.close()

            connection.close()