from pathlib import Path
import duckdb
import pyarrow as pa
from fastapi.responses import Response
import pandas as pd
import numpy as np
import lancedb
from typing import Dict, Callable, Optional, Tuple
from texture.models import (
    DuckQueryData,
    DuckQueryResult,
    ExecResponse,
    JsonResponse,
    ErrorResponse,
    DatasetSchema,
)
from texture.names import C_VECTOR

# NOTE: this path is affected by where the server is run from, assuming it is run in the root for now
CACHE_DIR = ".texture_cache/"
CACHE_PATH = Path(CACHE_DIR)
CACHE_PATH.mkdir(parents=True, exist_ok=True)


class DatabaseConnection:
    def __init__(self, database_name="defaultDatabase.db"):
        # Path(CACHE_PATH).mkdir(parents=True, exist_ok=True)
        # p = Path(CACHE_PATH) / database_name

        # NOTE: can save this to file, but potentially causes issues with old tables
        # so right now making new database on start up each time
        self.connection = duckdb.connect()

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
        self.execute(
            f"CREATE TABLE IF NOT EXISTS '{dataset_name}' AS (SELECT * FROM read_parquet('{CACHE_PATH / dataset_path}'));"
        )

    def load_dataframe(self, table_name, df: pd.DataFrame):
        """
        Loads a DataFrame into the database

        Args:
            dataset_name: name of the dataset
            df: DataFrame to load
        """
        q = f"CREATE TABLE '{table_name}' AS SELECT * FROM df"
        self.execute(q)

    def add_column(self, tableName, columnName, data):
        """
        Add a new column to the table with the given data. Data must match the length of the table.

        Args:
            tableName: name of the dataset
            columnName: NEW column name to add
            data: data to add. Can be list-like or pd.Series
        """

        # get current data
        current_df = self.connection.execute(f"SELECT * FROM {tableName}").fetchdf()
        current_df[columnName] = data

        # modify existing table
        viewName = f"{tableName}_TEMP_NEW"

        self.connection.register(viewName, current_df)
        self.connection.execute(
            f"CREATE OR REPLACE TABLE {tableName} as SELECT * FROM {viewName}"
        )
        self.connection.execute(f"DROP VIEW IF EXISTS {viewName}")

    def write_table_to_file(self, table_name, file_path):
        self.connection.execute(
            f"""COPY (SELECT * FROM "{table_name}") TO '{CACHE_PATH / file_path}' (FORMAT 'parquet');"""
        )

    def _handle_json_message(self, data: DuckQueryData) -> DuckQueryResult:
        """
        From: https://github.com/uwdata/mosaic/blob/main/packages/widget/mosaic_widget/__init__.py
        """
        uuid = data.uuid
        sql = data.sql
        response_message = None

        try:
            if data.type == "exec":
                self.connection.execute(sql)
                response_message = ExecResponse(type="exec", uuid=uuid)
            elif data.type == "json":
                query_result = self.connection.query(sql).df()

                # ensure if array data that is serializable
                query_result = query_result.map(
                    lambda x: x.tolist() if isinstance(x, np.ndarray) else x
                )

                json = query_result.to_dict(orient="records")

                response_message = JsonResponse(type="json", uuid=uuid, result=json)

            else:
                response_message = ErrorResponse(
                    error=f"Unsupported response type: {data.type}", uuid=uuid
                )

        except Exception as e:
            print("[Handle JSON message ERROR]: ", e, "\nExecuting SQL: ", sql)
            response_message = ErrorResponse(error=str(e), uuid=uuid)

        return response_message

    def _handle_arrow_message(self, data: DuckQueryData):
        """
        Arrow handler. Different function since returns Response; might be able to coalese in future
        """
        uuid = data.uuid
        sql = data.sql
        response_message = None

        try:
            if data.type == "arrow":
                query_result = self.connection.query(sql).arrow()

                sink = pa.BufferOutputStream()

                with pa.ipc.new_stream(sink, query_result.schema) as writer:
                    writer.write(query_result)

                pybytes = sink.getvalue().to_pybytes()
                response_message = Response(
                    content=pybytes,
                    media_type="application/vnd.apache.arrow.stream",
                )

            else:
                response_message = ErrorResponse(
                    error=f"Unsupported response type: {data.type}", uuid=uuid
                )
        except Exception as e:
            print("[Handle Arrow message ERROR]: ", e, "\nExecuting SQL: ", sql)
            response_message = ErrorResponse(error=str(e), uuid=uuid)

        return response_message


class VectorDBConnection:
    def __init__(self, database_dir="lancedb"):
        """
        embed_func: function that takes a string and returns a numpy array embedding.
        This MUST be same model as original embeddings or else comparison will not work
        """

        self.connection = lancedb.connect(CACHE_PATH / database_dir)
        self.id_cols = {}
        self.embed_funcs = {}  # type: dict[str, callable]

    def _check(self, table_name, check_conn=False, check_id=False, check_embed=False):
        if check_conn and table_name not in self.connection:
            raise ValueError(f"Table {table_name} not found in LanceDB.")

        if check_id and table_name not in self.id_cols:
            raise ValueError(f"Table {table_name} does not have an id column saved.")

        if check_embed and (
            table_name not in self.embed_funcs or self.embed_funcs[table_name] is None
        ):
            raise ValueError(
                f"Table {table_name} does not have a function for calcuating embeddings!"
            )

    def add_table(
        self,
        table_name: str,
        data: pd.DataFrame,
        id_col_name: str,
        embed_func: Optional[Callable] = None,
    ):
        """
        Add a table to the database.

        Args:
            table_name (str): The name of the table.
            data (pd.DataFrame): The dataframe containing the metadata. MUST have a column called "vector" with numpy arrays per row representing the vector representation.
            id_col_name (str): The name of the column in the dataframe that contains the unique identifier for each row.
            embed_func: function that takes a string and returns a numpy array embedding for this table

        Returns:
            None
        """
        # data[C_VECTOR] = list(embeddings)
        self.table = self.connection.create_table(
            table_name, data=data, mode="overwrite"
        )
        self.id_cols[table_name] = id_col_name
        self.embed_funcs[table_name] = embed_func

    def search(self, table_name: str, vector: np.array, limit: int = None):
        """
        Find ids of KNN docs to vector
        """
        self._check(table_name, check_conn=True, check_id=True)

        id_col = self.id_cols[table_name]
        vector_table = self.connection[table_name]

        # FUTURE: might be able to not use all rows but quant charts need no nulls rn
        if limit is None:
            limit = vector_table.count_rows()

        result = vector_table.search(vector).limit(limit).select([id_col])

        return result.to_pandas()[[id_col, "_distance"]]

    def get_embedding_from_string(self, table_name, text: str) -> np.array:
        self._check(table_name, check_embed=True)

        return self.embed_funcs[table_name](text)

    def get_embedding_from_id(self, table_name, id: str) -> np.array:
        """
        Get the embedding from the table by id
        """
        self._check(table_name, check_conn=True, check_id=True)

        df = (
            self.connection[table_name]
            .search()
            .where(f"{self.id_cols[table_name]} = {id}")
            .to_pandas()[C_VECTOR]
        )

        return df.iloc[0]


def initialize_databases(
    schema: DatasetSchema,
    load_tables: Dict[str, pd.DataFrame],
    create_new_embedding_func: Optional[Callable] = None,
) -> Tuple[DatabaseConnection, VectorDBConnection]:
    # Make DB
    duckdb_conn = DatabaseConnection()
    vectordb_conn = VectorDBConnection()

    # load vector data first
    if schema.has_embeddings:
        vectordb_conn.add_table(
            schema.name,
            load_tables[schema.name],
            schema.primary_key.name,
            create_new_embedding_func,
        )

        # remove vector column
        load_tables[schema.name] = load_tables[schema.name].drop(columns=[C_VECTOR])

    # Load data
    for table_name, table_df in load_tables.items():
        duckdb_conn.load_dataframe(table_name, table_df)

    return duckdb_conn, vectordb_conn
