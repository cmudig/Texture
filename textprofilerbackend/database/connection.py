from pathlib import Path
import time
import duckdb
import pyarrow as pa
from textprofilerbackend.models import (
    DuckQueryData,
    DuckQueryResult,
    ExecResponse,
    JsonResponse,
    ErrorResponse,
)
from fastapi.responses import Response
from textprofilerbackend.example_data import EXAMPLE_DATASETS
import pandas as pd

# NOTE: this path is affected by where the server is run from, assuming it is run in textprofilerbackend for now
CACHE_PATH = ".textprofiler_cache/"


def init_db():
    duckdbconn = DatabaseConnection()

    print("Loading example data...")

    datasetPaths = {
        "vast2021": "raw_data/vast2021.parquet",
        "dolly": "raw_data/dolly15k.parquet",
        "opus": "raw_data/opus100_en_es.parquet",
        "squad": "raw_data/squad_validation.parquet",
        "bbc": "raw_data/bbc_with_lava.parquet",
    }

    metadataCache = {}

    # load example datasets into duckdb
    for datasetInfo in EXAMPLE_DATASETS:
        dsName = datasetInfo.name
        duckdbconn.load_dataset(dsName, datasetPaths[dsName])
        metadataCache[dsName] = datasetInfo

    print("Example data loaded.")

    return duckdbconn, metadataCache


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

        # TODO: should maybe use the register function, especially for arrow data like parquet?
        #  See: https://duckdb.org/docs/archive/0.9.2/api/python/data_ingestion#dataframes--arrow-tables

        self.execute(
            f"CREATE TABLE IF NOT EXISTS '{dataset_name}' AS (SELECT * FROM read_parquet('{str(p)}'));"
        )

    def load_dataframe(self, dataset_name, df: pd.DataFrame):
        """
        Loads a DataFrame into the database

        Args:
            dataset_name: name of the dataset
            df: DataFrame to load
        """
        self.connection.register(dataset_name, df)
        print("registed new dataset in duckdb:  ", dataset_name)

    def _handle_json_message(self, data: DuckQueryData) -> DuckQueryResult:
        """
        From: https://github.com/uwdata/mosaic/blob/main/packages/widget/mosaic_widget/__init__.py
        """
        uuid = data.uuid
        sql = data.sql
        # start = time.time()
        response_message = None

        try:
            if data.type == "exec":
                self.connection.execute(sql)
                response_message = ExecResponse(type="exec", uuid=uuid)
            elif data.type == "json":
                query_result = self.connection.query(sql).df()
                json = query_result.to_dict(orient="records")

                response_message = JsonResponse(type="json", uuid=uuid, result=json)

            else:
                response_message = ErrorResponse(
                    error=f"Unsupported response type: {data.type}", uuid=uuid
                )

        except Exception as e:
            print("ERROR: ", e)
            response_message = ErrorResponse(error=str(e), uuid=uuid)

        # total = round((time.time() - start) * 1_000)
        # print(f"DONE. Query { uuid } took { total } ms.\n{ sql }")
        return response_message

    def _handle_arrow_message(self, data: DuckQueryData):
        """
        Arrow handler. Different function since returns Response; might be able to coalese in future
        """
        uuid = data.uuid
        sql = data.sql
        # start = time.time()
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
                    # headers={"type": "arrow", "uuid": uuid}, # dont think this does anything
                )

            else:
                response_message = ErrorResponse(
                    error=f"Unsupported response type: {data.type}", uuid=uuid
                )
        except Exception as e:
            print("ERROR: ", e)
            response_message = ErrorResponse(error=str(e), uuid=uuid)

        # total = round((time.time() - start) * 1_000)
        # print(f"DONE. Query { uuid } took { total } ms.\n{ sql }")

        return response_message
