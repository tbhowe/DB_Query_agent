#%%
import yaml
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

class DatabaseConnector:
    """A utility class for managing database operations.

    This class provides static methods for connecting to a database, reading credentials,
    uploading data, listing tables, reading tables, and executing select queries using SQLAlchemy.
    
    Attributes:
        None
    """

    def __init__(self):
        load_dotenv()

    @staticmethod
    def read_db_creds(filename):
        """Reads database credentials from a YAML file.

        Args:
            filename (str): File path of the YAML file containing database credentials.

        Returns:
            dict: A dictionary containing the database credentials.
        """
        with open(filename, "r") as stream:
            creds= yaml.safe_load(stream)
        return creds

    @staticmethod
    def init_db_engine(creds):
        """Initializes and returns a SQLAlchemy engine.

        Args:
            creds (dict): A dictionary containing database credentials.

        Returns:
            Engine: A SQLAlchemy Engine object.
        """
        engine = create_engine(f"{'postgresql'}+{'psycopg2'}://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}")
        engine.connect()
        return engine

    @staticmethod
    def list_db_tables(engine):
        """Lists all table names in the connected database.

        Args:
            engine (Engine): A SQLAlchemy Engine object.

        Returns:
            list: A list of table names.
        """
        inspector = inspect(engine)
        return inspector.get_table_names()

    @staticmethod
    def read_rds_table(engine, table_name: str):
        """Reads a table from the database and returns it as a Pandas DataFrame.

        Args:
            engine (Engine): A SQLAlchemy Engine object.
            table_name (str): The name of the table to read.

        Returns:
            DataFrame: A DataFrame containing the data from the specified table.
        """
        return pd.read_sql_table(table_name, engine)
    
    @staticmethod
    def execute_query(engine, query: str):
        """Executes a SELECT query and returns the result.

        Args:
            engine (Engine): A SQLAlchemy Engine object.
            query (str): A SQL query string (must be a SELECT statement).

        Returns:
            list: A list of rows returned by the query, where each row is a tuple.

        Raises:
            ValueError: If the query is not a SELECT statement.
            SQLAlchemyError: If an error occurs during query execution.
        """
        # Check if the query is a SELECT statement
        if not query.strip().lower().startswith("select"):
            raise ValueError("Only SELECT statements are allowed")

        try:
            with engine.connect() as connection:
                result = connection.execute(query)
                return [row for row in result]
        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")
            raise

class AgentHandler:
    def __init__(self):
        pass

    def get_table_list(self):
        pass

    def get_table_schema(self):
        pass
    
# test suite
if __name__== '__main__':
    db_yaml_file='prod_creds.yaml'
    creds = DatabaseConnector.read_db_creds(db_yaml_file)
    engine=DatabaseConnector.init_db_engine(creds)
    table_list=DatabaseConnector.list_db_tables(engine)
    print(table_list)

    
# %%
