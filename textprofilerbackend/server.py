from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from textprofilerbackend.database import DatabaseConnection
from textprofilerbackend.models import DatasetInfo, DuckQueryData, DuckQueryResult
from textprofilerbackend.example_data import EXAMPLE_DATASETS


def custom_generate_unique_id(route: APIRoute):
    """
    Replaces default generated name for TS objects with camel-cased method name.
    So python function `read_item` -> readItem
    NOTE: must ensure that route names are unique or will cause issues!
    """
    return route.name


def init_db():
    duckdbconn = DatabaseConnection()

    print("Loading example data...")

    datasets = [
        {"name": "dolly", "path": "raw_data/dolly15k.parquet"},
        {"name": "opus", "path": "raw_data/opus100_en_es.parquet"},
        {"name": "squad", "path": "raw_data/squad_validation.parquet"},
        {"name": "vast2021", "path": "raw_data/vast2021.parquet"},
    ]

    # TODO load some example datasets into memory?
    for dataset in datasets:
        duckdbconn.load_dataset(dataset["name"], dataset["path"])

    print("Example data loaded.")

    return duckdbconn


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
