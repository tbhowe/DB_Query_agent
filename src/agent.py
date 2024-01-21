#%%
from langchain.chat_models import ChatOpenAI
from langchain.prompts import(
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate
)
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv
from tools.sql import run_query_tool, list_tables_tool, list_columns_tool
from agent_tools import DatabaseConnector

connector = DatabaseConnector('prod_creds.yaml')
db_tables_list = str(connector.list_db_tables())
load_dotenv()
chat = ChatOpenAI()
prompt = ChatPromptTemplate(
    messages = [
        SystemMessagePromptTemplate.from_template("""You are an AI agent that can access a postgres database. 
                                                   The available tables in the database are: {db_tables_list}
                                                   You also have access to the following tools: {tools_list},
                                                  """),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)
tools = [run_query_tool, list_tables_tool, list_columns_tool]
agent = OpenAIFunctionsAgent(
    llm = chat,
    prompt = prompt,
    tools = tools
)
 
agent_executor = AgentExecutor(
    agent = agent,
    verbose = True,
    tools = tools

)

agent_executor("how many users are on the DevOps Engineering Specialisation journey?")
# %%