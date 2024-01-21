#%%
import yaml
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

class DatabaseConnector:

    def __init__(self):
        load_dotenv()

    @staticmethod
    def read_db_creds(filename):
        ''' takes YAML filepath and returns a dict of the database credentials'''
        with open(filename, "r") as stream:
            creds= yaml.safe_load(stream)
        return creds

    @staticmethod
    def init_db_engine(creds):
        '''take data from read_db_creds, return sqlalchemy database engine'''
        engine = create_engine(f"{'postgresql'}+{'psycopg2'}://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}")
        engine.connect()
        return engine

    @staticmethod
    def upload_to_db(engine, df , table_name: str):
        '''takes in table name and dataframe, converts to SQL and replaces in database'''
        df.to_sql(table_name, engine, if_exists='replace')
        pass

    @staticmethod
    def list_db_tables(engine):
        '''takes in an engine object and returns a list of table names in the database'''
        inspector = inspect(engine)
        return inspector.get_table_names()

    @staticmethod
    def read_rds_table(engine, table_name: str):
        '''takes a table name as string, and an engine object and returns the table as a PANDAS df '''
        return pd.read_sql_table(table_name, engine)
    
    @staticmethod
    def execute_query(engine, query: str):
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
