from langchain.tools import Tool
from agent_tools import DatabaseConnector

run_query_tool = Tool.from_function(
                                    name = "run_sql_query",
                                    description = "Run a postgresql SELECT query, returns the result of the query.",
                                    func = DatabaseConnector.execute_query
                                    )

list_tables_tool = Tool.from_function(
                                    name = "list_tables",
                                    description = "List all tables in the database. Returns the table names.",
                                    func = DatabaseConnector.list_db_tables
                                    )

list_columns_tool = Tool.from_function(
                                    name = "list_columns",
                                    description = "Given a table name as an input, List all columns in a table. Returns the column names.",
                                    func = DatabaseConnector.get_table_columns
                                    )
