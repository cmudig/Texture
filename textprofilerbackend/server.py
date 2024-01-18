from fastapi import FastAPI, UploadFile, File
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from typing import Dict

from textprofilerbackend.database import init_db
from textprofilerbackend.models import (
    DatasetInfo,
    DuckQueryData,
    DuckQueryResult,
    DatasetUploadResponse,
    DatasetVerifyResponse,
)
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

    duckdb_conn, datasetMetadataCache = init_db()

    # TODO this is prob need to use actual cache here rather than just in memory
    datasetUploadCache = {}

    @api_app.get(
        "/",
        response_model=str,
    )
    def root_status():
        return "hello"

    @api_app.get(
        "/all_dataset_info",
        response_model=Dict[str, DatasetInfo],
    )
    def read_dataset_info():
        """
        Get the datasets available along with a summary of their columns
        """

        return datasetMetadataCache

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

    @api_app.post("/upload_dataset", response_model=DatasetUploadResponse)
    async def upload_dataset(file: UploadFile = File(...)):
        # TODO: support huggingface datasets
        if file.filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(await file.read()))
            datasetName = file.filename[:-4]
        elif file.filename.endswith(".parquet"):
            df = pd.read_parquet(BytesIO(await file.read()))
            datasetName = file.filename[:-8]
        else:
            return DatasetUploadResponse(
                success=False,
                message=f"Unsupported file type for '{file.filename}'. Only CSV and Parquet files are supported.",
            )

        # Process the DataFrame
        initial_dataset_info = process_new_file(df, datasetName)

        datasetUploadCache[datasetName] = df
        datasetMetadataCache[datasetName] = initial_dataset_info

        return DatasetUploadResponse(
            success=True,
            message="File processed successfully",
            datasetSchema=initial_dataset_info,
        )

    @api_app.post("/verify_schema", response_model=DatasetVerifyResponse)
    async def verify_schema(schema: DatasetInfo):
        print("HIT: verify_schema")
        name = schema.name
        print("veriyfing schmea: ", name)

        if name in datasetMetadataCache and name in datasetUploadCache:
            print("found in cache schmea: ")

            datasetMetadataCache[name] = schema
            duckdb_conn.load_dataframe(name, datasetUploadCache[name])

            # clear out so not in memory again (hopefully doesnt mess up duckdb...)
            # del datasetUploadCache[name]

            return DatasetVerifyResponse(
                success=True, message="Schema verified and uploaded."
            )

        return DatasetVerifyResponse(
            success=False,
            message=f"Failed to update schema for unknown dataset: {name}",
        )

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
