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
import numpy as np
import lancedb
import torch
import sentence_transformers

# NOTE: this path is affected by where the server is run from, assuming it is run in textprofilerbackend for now
CACHE_PATH = ".textprofiler_cache/"


def get_embedding(col: np.ndarray, model_name):
    model = sentence_transformers.SentenceTransformer(model_name)
    e = model.encode(col)
    return e


def init_db():
    duckdbconn = DatabaseConnection()
    vectordbconn = VectorDBConnection()

    print("Loading duckdb data...")
    datasetPaths = {
        "vast2021": "raw_data/vast_w_id.parquet",
        "vast2021_word": "raw_data/vast_word_w_id.parquet"
        # "dolly": "raw_data/dolly15k.parquet",
        # "opus": "raw_data/opus100_en_es.parquet",
        # "squad": "raw_data/squad_validation.parquet",
        # "bbc": "raw_data/bbc_with_lava.parquet",
    }
    metadataCache = {}
    # load example datasets into duckdb
    # for datasetInfo in EXAMPLE_DATASETS:
    #     dsName = datasetInfo.name
    #     duckdbconn.load_dataset(dsName, datasetPaths[dsName])
    #     metadataCache[dsName] = datasetInfo

    # TEMP: load example data
    duckdbconn.load_dataset("vast2021", "raw_data/vast_w_id.parquet")
    duckdbconn.load_dataset("vast2021_word", "raw_data/vast_word_w_id.parquet")
    duckdbconn.load_dataset("vis_papers", "raw_data/vis_papers/vis_papers.parquet")
    duckdbconn.load_dataset(
        "vis_papers_words", "raw_data/vis_papers/vis_papers_words.parquet"
    )
    metadataCache["vis_papers"] = EXAMPLE_DATASETS[0]
    metadataCache["vast2021"] = EXAMPLE_DATASETS[1]

    print("Loading vector data...")
    vis_paper_embeddings = torch.load(
        ".textprofiler_cache/raw_data/vis_papers/vis_papers_embeddings.pt"
    )
    vis_paper_df = pd.read_parquet(
        ".textprofiler_cache/raw_data/vis_papers/vis_papers.parquet"
    )
    vis_paper_df["vector"] = list(vis_paper_embeddings.numpy())
    embed_func = lambda x: get_embedding(x, "all-mpnet-base-v2")

    vectordbconn.add_table("vis_papers", vis_paper_df, "id", embed_func)

    print("Example data loaded.")

    return duckdbconn, vectordbconn, metadataCache


class DatabaseConnection:
    def __init__(self, database_name="defaultDatabase.db"):
        # Path(CACHE_PATH).mkdir(parents=True, exist_ok=True)
        # p = Path(CACHE_PATH) / database_name

        print("Making new DuckDB DatabaseConnection in memory")

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
            print("[Handle JSON message ERROR]: ", e, "\nExecuting SQL: ", sql)
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
            print("[Handle Arrow message ERROR]: ", e, "\nExecuting SQL: ", sql)
            response_message = ErrorResponse(error=str(e), uuid=uuid)

        # total = round((time.time() - start) * 1_000)
        # print(f"DONE. Query { uuid } took { total } ms.\n{ sql }")

        return response_message


class VectorDBConnection:
    def __init__(self, database_dir="lancedb"):
        """
        embed_func: function that takes a string and returns a numpy array embedding.
        This MUST be same model as original embeddings or else comparison will not work
        """
        Path(CACHE_PATH).mkdir(parents=True, exist_ok=True)
        p = Path(CACHE_PATH) / database_dir

        print("Making new LanceDB connection")

        self.connection = lancedb.connect(p)
        self.id_cols = {}
        self.embed_funcs = {}

    def _check(self, table_name, check_conn=False, check_id=False, check_embed=False):
        if check_conn and table_name not in self.connection:
            raise ValueError(f"Table {table_name} not found in LanceDB.")

        if check_id and table_name not in self.id_cols:
            raise ValueError(f"Table {table_name} does not have an id column saved.")

        if check_embed and table_name not in self.embed_funcs:
            raise ValueError(f"Table {table_name} does not have an embedding function.")

    def add_table(
        self, table_name: str, data: pd.DataFrame, id_col_name: str, embed_func
    ):
        """
        Add a table to the database.

        Args:
            table_name (str): The name of the table.
            data (pd.DataFrame): The dataframe containing the metadata and a column called "vector" with numpy arrays per row representing the vector representation.
            id_col_name (str): The name of the column in the dataframe that contains the unique identifier for each row.
            embed_func: function that takes a string and returns a numpy array embedding for this table

        Returns:
            None
        """
        self.table = self.connection.create_table(
            table_name, data=data, mode="overwrite"
        )
        self.id_cols[table_name] = id_col_name
        self.embed_funcs[table_name] = embed_func

    def search(self, table_name: str, vector: np.array, limit: int = 20):
        """
        Find ids of KNN docs to vector
        """
        self._check(table_name, check_conn=True, check_id=True)

        id_col = self.id_cols[table_name]
        result = (
            self.connection[table_name].search(vector).limit(limit).select([id_col])
        )

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
            .to_pandas()["vector"]
        )

        return df.iloc[0]
