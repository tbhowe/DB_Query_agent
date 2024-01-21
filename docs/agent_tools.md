
# DatabaseConnector Class

The `DatabaseConnector` class is a utility for managing database operations using SQLAlchemy in Python. It simplifies tasks such as connecting to the database, reading data, and executing queries.

## Class Methods

### `__init__()`
Initializes the DatabaseConnector instance. It automatically loads environment variables.

```python
def __init__(self):
```

### `read_db_creds(filename)`
Reads database credentials from a YAML file.

- `filename`: File path of the YAML file containing database credentials.

```python
@staticmethod
def read_db_creds(filename):
```

### `init_db_engine(creds)`
Initializes and returns a SQLAlchemy engine using the provided credentials.

- `creds`: A dictionary containing database credentials.

```python
@staticmethod
def init_db_engine(creds):
```

### `upload_to_db(engine, df, table_name)`
Uploads a Pandas DataFrame to a SQL database, replacing the table if it exists.

- `engine`: SQLAlchemy engine object.
- `df`: Pandas DataFrame to be uploaded.
- `table_name`: Name of the table to which the DataFrame should be uploaded.

```python
@staticmethod
def upload_to_db(engine, df, table_name):
```

### `list_db_tables(engine)`
Returns a list of table names available in the database.

- `engine`: SQLAlchemy engine object.

```python
@staticmethod
def list_db_tables(engine):
```

### `read_rds_table(engine, table_name)`
Reads a table from the database and returns it as a Pandas DataFrame.

- `engine`: SQLAlchemy engine object.
- `table_name`: Name of the table to be read.

```python
@staticmethod
def read_rds_table(engine, table_name):
```

### `execute_query(engine, query)`
Executes a `SELECT` SQL query and returns the result.

- `engine`: SQLAlchemy engine object.
- `query`: SQL query string (must be a `SELECT` statement).

```python
@staticmethod
def execute_query(engine, query):
```

## Usage Example

```python
connector = DatabaseConnector()
creds = connector.read_db_creds("path/to/creds.yaml")
engine = connector.init_db_engine(creds)

# Upload DataFrame to database
connector.upload_to_db(engine, df, "table_name")

# List tables in the database
tables = connector.list_db_tables(engine)
print(tables)

# Read a table into a DataFrame
dataframe = connector.read_rds_table(engine, "table_name")
print(dataframe)

# Execute a SELECT query
results = connector.execute_query(engine, "SELECT * FROM table_name")
print(results)
```

## Important Notes

- Ensure that the YAML file containing database credentials is secure and not exposed. If you have forked or cloned this project, ensure that your creds file is added to your `.gitignore`
- The `execute_query` method only allows `SELECT` statements for security reasons. Attempts to execute other types of SQL statements will result in a `ValueError`.
```
