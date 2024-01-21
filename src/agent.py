from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv
from tools.sql import run_query_tool, list_tables_tool, list_columns_tool
from agent_tools import DatabaseConnector
import os

class AgentExecutorWrapper:
    """Wrapper class for setting up and executing an AI agent with database access.

    This class encapsulates the functionality related to initializing and running an AI agent
    that can execute queries against a PostgreSQL database and utilize specified tools.

    Attributes:
        connector (DatabaseConnector): Instance to interact with the database.
        db_tables_list (list): List of tables available in the database.
        agent (OpenAIFunctionsAgent): The AI agent initialized with a chat model and prompt.
    """
    def __init__(self, db_creds_file):
        """Initializes the AgentExecutorWrapper with database credentials and tools.

        Args:
            db_creds_file (str): The file path for the database credentials YAML file.
            tools (list): A list of callable tools that the agent can use.
        """

        self.connector = DatabaseConnector(db_creds_file)
        self.db_tables_list = self.connector.list_db_tables()
        self.tools = [run_query_tool, list_tables_tool, list_columns_tool]
        self.agent = self._initialize_agent()

    def _initialize_agent(self):
        """Initializes the AI agent with a chat model and a prompt template.

        This method sets up the chat model and the prompt template to be used by the AI agent.
        It uses the database tables and tools information for the prompt.

        Returns:
            OpenAIFunctionsAgent: The initialized AI agent.
        """

        load_dotenv()
        chat_model = ChatOpenAI()
        prompt = ChatPromptTemplate(
            messages=[
                SystemMessage(content=f"""You are an AI agent that can access a postgres database. 
                                           The available tables in the database are: {self.db_tables_list}
                                           You also have access to the following tools: {self.tools},
                                          """),
                HumanMessagePromptTemplate.from_template("{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ]
        )
        return OpenAIFunctionsAgent(
            llm=chat_model,
            prompt=prompt,
            tools=self.tools
        )

    def execute(self, query):
        """Executes a query using the agent.

        This method uses the AgentExecutor to run a given query through the AI agent.

        Args:
            query (str): The query or command to be executed by the agent.

        Returns:
            Any: The result of the query execution by the agent.
        """

        agent_executor = AgentExecutor(
            agent=self.agent,
            verbose=True,
            tools=self.tools
        )
        return agent_executor(query)

# Usage
if __name__ == "__main__":
    db_creds_file = 'prod_creds.yaml'
    agent_executor_wrapper = AgentExecutorWrapper(db_creds_file)
    result = agent_executor_wrapper.execute("how many users are on the DevOps Engineering Specialisation journey?")
    print(result)
