def create_table_schema(columns):
    return {
        "columns": columns,
        "primary_keys": [],
        "foreign_keys": []
    }

def assemble_schema(columns, primary_keys, foreign_keys):
    schema = {}

    for table_name, table_columns in columns.items():
        schema[table_name] = create_table_schema(table_columns)
    
    for table_name, keys in primary_keys.items():
        if table_name in schema:
            schema[table_name]["primary_keys"] = keys

    for table_name, keys in foreign_keys.items():
         if table_name in schema:
            schema[table_name]["foreign_keys"] = keys

    return schema