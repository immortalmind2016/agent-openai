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