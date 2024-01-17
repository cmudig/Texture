from fastapi import FastAPI, UploadFile, File
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from textprofilerbackend.database import init_db
from textprofilerbackend.models import (
    DatasetInfo,
    DuckQueryData,
    DuckQueryResult,
    GenericResponse,
)
from textprofilerbackend.example_data import EXAMPLE_DATASETS
from textprofilerbackend.process_data import process_new_file

from io import BytesIO
import pandas as pd


def custom_generate_unique_id(route: APIRoute):
    """
    Replaces default generated name for TS objects with camel-cased method name.
    So python function `read_item` -> readItem
    NOTE: must ensure that route names are unique or will cause issues!
    """
    return route.name


def get_server() -> FastAPI:
    app = FastAPI(
        title="Backend server",
    )

    api_app = FastAPI(
        title="Text Profiler API",
        generate_unique_id_function=custom_generate_unique_id,
        # TODO: unsure if this is necessary...
        default_response_class=ORJSONResponse,
    )

    duckdb_conn = init_db()

    @api_app.get(
        "/dataset_names",
        response_model=list[str],
    )
    def read_all_dataset_names():
        r = duckdb_conn.query("show tables;")
        return ["dolly", "opus", "squad", "vast2021"]

    @api_app.get(
        "/all_dataset_info",
        response_model=list[DatasetInfo],
    )
    def read_dataset_info():
        """
        Get the datasets available along with a summary of their columns
        """

        return EXAMPLE_DATASETS

    @api_app.post("/duckdb_query_json", response_model=DuckQueryResult)
    def duckdb_query_json(data: DuckQueryData):
        """
        Execute a query on the database
        """
        return duckdb_conn._handle_json_message(data)

    @api_app.post("/duckdb_query_arrow")
    async def duckdb_query_arrow(data: DuckQueryData):
        """
        Execute a query on the database
        """
        return duckdb_conn._handle_arrow_message(data)

    @api_app.post("/upload_dataset", response_model=GenericResponse)
    async def upload_dataset(file: UploadFile = File(...)):
        # Check if the file is CSV or Parquet
        if file.filename.endswith(".csv"):
            # For CSV files
            df = pd.read_csv(BytesIO(await file.read()))
        elif file.filename.endswith(".parquet"):
            # For Parquet files
            df = pd.read_parquet(BytesIO(await file.read()))
        else:
            return GenericResponse(
                success=False,
                message=f"Unsupported file type for '{file.filename}'. Only CSV and Parquet files are supported.",
            )

        # Process the DataFrame
        process_new_file(df)

        return GenericResponse(success=True, message="File processed successfully")

    # @api_app.get("/example_arrow")
    # async def example_arrow():
    #     """
    #     Execute a query on the database
    #     """

    #     data = DuckQueryData(
    #         uuid="test",
    #         sql="select * from 'vast2021' limit 10;",
    #         type="arrow",
    #         buffers=[],
    #     )

    #     return duckdb_conn._handle_arrow_message(data)

    # this needs to be equal to frontend port vite hosts on...
    origins = ["http://localhost:5173"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.mount("/api", api_app)

    return app
