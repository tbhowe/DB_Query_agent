#%%
import yaml
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from sqlalchemy import text
import os



class DatabaseConnector:
    """A utility class for managing database operations.

    This class provides static methods for connecting to a database, reading credentials,
    uploading data, listing tables, reading tables, and executing select queries using SQLAlchemy.
    
    Attributes:
        None
    """


    def __init__(self, creds_path: str):
        self.creds_path = creds_path
        load_dotenv()
        self.init_db_engine(self.creds_path)
        

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

   
    def init_db_engine(self, filename):
        """Initializes the SQLAlchemy engine using database credentials from a YAML file.

        Args:
            filename (str): File path of the YAML file containing database credentials.

        Sets:
            self.engine: A SQLAlchemy Engine object.
        """
        creds = self.read_db_creds(filename)
        self.engine = create_engine(f"postgresql+psycopg2://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}")
        self.engine.connect()

    
    def list_db_tables(self, *args, **kwargs):
        """Lists all table names in the connected database.

        Args:
            engine (Engine): A SQLAlchemy Engine object.

        Returns:
            str: A list of table names, each on a newline
        """

        inspector = inspect(self.engine)
        table_names = inspector.get_table_names()
        return "\n".join(table_names)
    
    
    def get_table_columns(self, table_name: str):
        """Retrieves a list of column names for a specified table in the database.

        This method inspects the given database table and returns a list containing the names
        of all columns in that table.

        Args:
            engine (Engine): A SQLAlchemy Engine object representing the database connection.
            table_name (str): The name of the table for which to retrieve column names.

        Returns:
            list: A list of strings, where each string is a column name from the specified table.
        """

        inspector = inspect(self.engine)
        return [column['name'] for column in inspector.get_columns(table_name)]

    
    def execute_query(self, query: str):
        """Executes a SELECT query and returns the result.

        Args:
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
            with self.engine.connect() as connection:
                result = connection.execute(text(query))
                return [row for row in result]
        except SQLAlchemyError as e:
            return f"An error occurred when attempting to process the query: {e}"
            

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
    db_connector = DatabaseConnector(db_yaml_file)

    try:
        table_list = db_connector.list_db_tables()
        print("table list function working")
        print(table_list)
    except SQLAlchemyError as e:
        print(f"An error occurred in list_db_tables: {e}")
        raise
    
    try:
        table_columns = db_connector.get_table_columns('users')
        print("table columns function working")
    except SQLAlchemyError as e:
        print(f"An error occurred in get_table_columns: {e}")
        raise

    try: 
        query_result = db_connector.execute_query('SELECT * FROM users')
        print("execute query function working")

    except SQLAlchemyError as e:
        print(f"An error occurred in execute_query: {e}")
        raise

 

    
# %%
