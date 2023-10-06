from sql_metadata import Parser
import re


def dealias_tables(sql_query: str) -> str:
    """
    Remove aliases from the given sql_query and replace them with the original
    column and table names.

    Args:
        sql_query (str): A string of the SQL Query to be de-aliased.

    Returns:
        str: The SQL query with all aliases removed.
    """

    parser = Parser(sql_query)

    for table_alias, table_original in parser.tables_aliases.items():
        # Remove the alias declaration using regexp to guarrantee that the case
        # of the AS statement is ignored
        compiled = re.compile(re.escape(f" AS {table_alias}"), re.IGNORECASE)
        sql_query = compiled.sub("", sql_query)

        # Replace all uses of the alias with the original name
        sql_query = sql_query.replace(table_alias, table_original)

    return sql_query
