import sqlite3 
from langchain.tools import BaseTool, Tool


conn = sqlite3.connect('db.sqlite')

def run_sql_query(query: str) -> str:
    c=conn.cursor()
    try:
        c.execute(query)
        result = c.fetchall()
        return result
    except sqlite3.OperationalError as err:
        return f"The following error occurred: {err}"
run_query_tool = Tool.from_function(
    func=run_sql_query,
    name="run_sql_query",
    description="Run a SQL query on the example.db database. The query should be a valid SQL statement.",
)

def describe_table(tables_name) -> str:
    c=conn.cursor()
    tables=', '.join("'"+table[0]+"'" for table in tables_name)
    rows =c.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name IN ({tables});")
    return '\n'.join([row[0] for row in rows if row[0] is not None])

describe_table_tool = Tool.from_function(
    func=describe_table,
    name="describe_table",
    description="Describe the table structure of the example.db database. The table name should be a valid SQL statement.",
)