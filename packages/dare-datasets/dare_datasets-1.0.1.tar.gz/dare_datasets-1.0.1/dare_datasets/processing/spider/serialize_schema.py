import pandas as pd


def serialize_schema(schema: pd.DataFrame,
                     with_db_id: bool = True,
                     with_fp_relations: bool = False,
                     db_id: str = None,
                     db_id_sep: str = " | ",
                     table_sep: str = " | ",
                     table_column_sep: str = " : ",
                     column_sep: str = " , ",
                     fp_relations_sep: str = " | ",
                     fp_relation_sep: str = " , "
                     ) -> str:
    """
    Returns the schema of the db as a string.

    Args:
        schema (DataFrame): The schema json object of the database
        with_db_id (bool): If True the serialization will contain the id of the database
        with_fp_relations (bool): If True the serialization will contain the foreign-primary key relations of
                                  the schema
        db_id (str): The database id, which schema will be serialized
        db_id_sep (str): The separator string between the db id and the rest of the schema
        table_sep (str): The separation string between two tables of the schema
        table_column_sep (str): The separation string between a table and its columns
        column_sep (str): The separation string between two columns of the schema
        fp_relations_sep (str): The separation string between the foreign-primary key relations and the rest of
                                the schema
        fp_relation_sep (str): The separation string between two foreign-primary key relations of the schema

    Returns:
        str: The database schema in a string format
    """

    # Get the columns and the tables from the schema
    columns = schema["column_names_original"].iloc[0]
    table_names = schema["table_names_original"].iloc[0]

    serialized_tables = []
    # For each table
    for t_i, table in enumerate(table_names):
        # Get the columns of the current table
        table_columns = list(filter(lambda column: column[0] == t_i, columns))
        # Keep only the name of the columns
        table_columns_names = list(map(lambda column: column[1], table_columns))

        # Serialize the table and its columns
        serialized_table = f"{table_column_sep}".join([table, f"{column_sep}".join(table_columns_names)])
        serialized_tables.append(serialized_table)

    serialized_schema = f"{table_sep}".join(serialized_tables)

    # If the serialization contains foreign-primary key relations
    if with_fp_relations:
        fp_pairs = schema["foreign_keys"].iloc[0]
        if len(fp_pairs) > 0:
            serialized_fp_relations = []
            # For each foreign-primary key relation
            for foreign_key_id, primary_key_id in fp_pairs:
                # Get the foreign and primary key in a format: <table_name>.<column_name>
                foreign_key_name = f"{table_names[columns[foreign_key_id][0]]}.{columns[foreign_key_id][1]}"
                primary_key_name = f"{table_names[columns[primary_key_id][0]]}.{columns[primary_key_id][1]}"

                serialized_fp_relations.append(f"{foreign_key_name} = {primary_key_name}")

            # Append the fp-relations to the serialized schema
            serialized_schema += fp_relations_sep + f"{fp_relation_sep}".join(serialized_fp_relations)

    # If the db_id will be included in the schema serialization
    if with_db_id and db_id is not None:
        serialized_schema = f"{db_id}{db_id_sep}{serialized_schema}"

    return serialized_schema
