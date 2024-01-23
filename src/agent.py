from functools import partial
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from handlers.chat_model_start_handler import ChatModelStartHandler, boxen_print
from dotenv import load_dotenv
from tools.sql import run_query_tool, list_tables_tool, list_columns_tool
from tools.report import write_report_tool
from agent_tools import DatabaseConnector
import gradio as gr
import os
import logging
import sys




class AgentExecutorWrapper:
    """Wrapper class for setting up and executing an AI agent with database access.

    This class encapsulates the functionality related to initializing and running an AI agent
    that can execute queries against a PostgreSQL database and utilize specified tools.

    Attributes:
        connector (DatabaseConnector): Instance to interact with the database.
        db_tables_list (list): List of tables available in the database.
        agent (OpenAIFunctionsAgent): The AI agent initialized with a chat model and prompt.
    """
    def __init__(self):
        """Initializes the AgentExecutorWrapper with database tools.
        """

        self.connector = DatabaseConnector()
        self.db_tables_list = self.connector.list_db_tables()
        self.tools = [run_query_tool, list_tables_tool, list_columns_tool, write_report_tool]
        self.agent = self._initialize_agent()
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        

    def _initialize_agent(self):
        """Initializes the AI agent with a chat model and a prompt template.

        This method sets up the chat model and the prompt template to be used by the AI agent.
        It uses the database tables and tools information for the prompt.

        Returns:
            OpenAIFunctionsAgent: The initialized AI agent.
        """

        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        model_name='gpt-4-1106-preview'
        chat_model_start_handler = ChatModelStartHandler()
        chat_model = ChatOpenAI(temperature=0, model=model_name, callbacks=[chat_model_start_handler])
        prompt = ChatPromptTemplate(
            messages=[
                SystemMessage(content=f"""You are an AI agent that can access a postgres database. 
                                           The available tables in the database are: {self.db_tables_list}
                                           You also have access to the following tools: 
                                           ___
                                           - list_tables: returns the list of tables in the database. You do not need to supply an argument to this tool.
                                           - list_columns: returns the columns of a given table. You must supply a single table name as an argument to this tool.
                                           - run_sql_query: runs a postgresql SELECT query against the database and returns the result of the query
                                           - write_report: writes an HTML report to a file. Use this whenever someone asks for a report.
                                           ___
                                            Do not make any assumptions about what tables exist, or about what columns exist.
                                            Before you run a query, you should make sure to use the list_columns tool to get the schema of the tables you want to query, so that you don't make any mistakes.
                                          """),
                MessagesPlaceholder(variable_name="chat_history"),
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
            # verbose=True,
            tools=self.tools,
            memory=self.memory
        )
        return agent_executor(query)
    
    def query_agent(self, input_text):
        """Executes a query using the agent instance.

        Args:
            input_text (str): The query or command to be executed by the agent.

        Returns:
            str: The result of the query execution by the agent.
        """
        result = self.execute(input_text)
        return result.get('output', 'No output generated')
      # Fallback message if 'output' is not in result

# Usage
if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    agent_executor_wrapper = AgentExecutorWrapper()
    query_function = partial(agent_executor_wrapper.query_agent)
    iface = gr.Interface(
        fn=query_function,
        inputs=gr.Textbox(lines=2, placeholder="Enter your query here...", label="Your Query"),
        outputs="text",
        title="AiCore Database Query Agent",
        description="Enter a natural language query to get information from the database."
    )

    iface.launch(server_name="0.0.0.0", server_port=80, share=True)
    
