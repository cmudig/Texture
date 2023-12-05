import duckdb
from pathlib import Path


# NOTE: this path is affected by where the server is run from, assuming it is run in textprofilerbackend for now
CACHE_PATH = ".textprofiler_cache/"


class DatabaseConnection:
    def __init__(self, database_name="defaultDatabase.db"):
        Path(CACHE_PATH).mkdir(parents=True, exist_ok=True)
        p = Path(CACHE_PATH) / database_name

        print("Making new DatabaseConnection, saving to:  ", str(p))
        self.connection = duckdb.connect(str(p))

    def query(self, query_string: str) -> list:
        """
        Executes SQL query on database
        See other return types: https://duckdb.org/docs/archive/0.9.2/api/python/overview

        Returns:
            - Array of python objects representing rows
        """
        return self.connection.sql(query_string).fetchall()

    def execute(self, query_string: str) -> None:
        """
        Executes SQL that does not expect return.

        Returns:
            - None
        """
        self.connection.sql(query_string)

    def load_dataset(self, dataset_name: str, dataset_path: str):
        """
        Loads a dataset into the database

        Args:
            dataset_name: name of the dataset
            dataset_path: path to parquet file
        """
        p = Path(CACHE_PATH) / dataset_path

        self.execute(
            f"CREATE TABLE IF NOT EXISTS '{dataset_name}' AS (SELECT * FROM read_parquet('{str(p)}'));"
        )
        print("loaded: ", dataset_name)
