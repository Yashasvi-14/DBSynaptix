from app.sql.sql_validator import SQLValidator

responses = [

    "SELECT * FROM customers;",

    "```sql\nSELECT * FROM customers;\n```",

    "Here is the SQL query:\nSELECT * FROM customers;",

    "DROP TABLE customers;",

    "DELETE FROM orders;",

    "UPDATE customers SET city='Delhi';",

    "SCHEMA_NOT_FOUND"
]

validator = SQLValidator()

for response in responses:

    print("=" * 70)

    print(response)

    print()

    try:

        sql = validator.validate(response)

        print("VALID")

        print(sql)

    except Exception as e:

        print("REJECTED")

        print(e)