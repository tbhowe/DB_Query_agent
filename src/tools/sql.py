from langchain.tools import Tool
from agent_tools import DatabaseConnector

connector = DatabaseConnector('prod_creds.yaml')
print("connector created")

run_query_tool = Tool.from_function(
                                    name = "run_sql_query",
                                    description = "Run a postgresql SELECT query, returns the result of the query.",
                                    func = connector.execute_query
                                    )

list_tables_tool = Tool.from_function(
                                    name = "list_tables",
                                    description = "List all tables in the database. Returns the table names.",
                                    func = connector.list_db_tables
                                    )

list_columns_tool = Tool.from_function(
                                    name = "list_columns",
                                    description = "Given a table name as an input, Returns the column names for that table.",
                                    func = connector.get_table_columns
                                    )
