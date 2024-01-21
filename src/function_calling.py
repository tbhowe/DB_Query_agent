from langchain.tools import Tool
from agent_tools import DatabaseConnector

run_query_tool = Tool.from_function(
                                    name = "run_sql_query",
                                    description = "Run a postgresql SELECT query, returns the result of the query.",
                                    func = DatabaseConnector.execute_query
                                    )