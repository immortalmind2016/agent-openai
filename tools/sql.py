import sqlite3 
from langchain.tools import BaseTool, Tool
from pydantic import BaseModel
from typing import List

conn = sqlite3.connect('db.sqlite')

def list_tables():
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = c.fetchall()
    return "\n".join(row[0] for row in rows if row[0] is not None)

def run_sql_query(query: str) -> str:
    c=conn.cursor()
    try:
        c.execute(query)
        result = c.fetchall()
        return result
    except sqlite3.OperationalError as err:
        return f"The following error occurred: {err}"
    
class RunQueryArgsSchema(BaseModel):
    query: str
    
run_query_tool = Tool.from_function(
    func=run_sql_query,
    name="run_sql_query",
    args_schema=RunQueryArgsSchema,
    description="Run a SQL query on the example.db database. The query should be a valid SQL statement.",
)

def describe_tables(table_names):
    c = conn.cursor()
    tables = ', '.join("'" + table + "'" for table in table_names)
    rows = c.execute(f"SELECT sql FROM sqlite_master WHERE type='table' and name IN ({tables});")
    return '\n'.join(row[0] for row in rows if row[0] is not None)


class DescribeTablesArgsSchema(BaseModel):
    tables_names: List[str]


describe_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of table names, returns the schema of those tables",
    func=describe_tables,
    args_schema=DescribeTablesArgsSchema
)
