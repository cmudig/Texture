from fastapi import FastAPI, UploadFile, File
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from typing import Dict, Literal


from textprofilerbackend.database import init_db
from textprofilerbackend.models import (
    DatasetInfo,
    DuckQueryData,
    DuckQueryResult,
    DatasetUploadResponse,
    DatasetVerifyResponse,
    DatasetTokenizeResponse,
    VectorSearchResponse,
    LLMResponse,
    LLMTransformRequest,
    LLMTransformCommit,
    Column,
)
from textprofilerbackend.process_data import process_new_file
from textprofilerbackend.transform import word_tokenize
from textprofilerbackend.llm.client import LLMClient
from textprofilerbackend.utils import process_results, get_type_from_response

from io import BytesIO
import pandas as pd
import datetime


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

    duckdb_conn, vectordb_conn, datasetMetadataCache = init_db()
    llm_client = LLMClient()

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

        return DatasetUploadResponse(
            success=True,
            message="File processed successfully",
            datasetSchema=initial_dataset_info,
        )

    @api_app.post("/verify_schema", response_model=DatasetVerifyResponse)
    async def verify_schema(new_schema: DatasetInfo, originalName: str):
        if originalName in datasetUploadCache:
            new_name = new_schema.name
            datasetMetadataCache[new_name] = new_schema
            duckdb_conn.load_dataframe(new_name, datasetUploadCache[originalName])

            # clear out cache once put in duckdb
            del datasetUploadCache[originalName]

            return DatasetVerifyResponse(
                success=True, message="Schema verified and uploaded."
            )

        return DatasetVerifyResponse(
            success=False,
            message=f"Failed to update schema for unknown dataset: {originalName}",
        )

    @api_app.post("/tokenize_dataset", response_model=DatasetTokenizeResponse)
    async def tokenize_dataset(
        datasetName: str, columnName: str, tokenType: Literal["word", "token"]
    ):
        if datasetName in datasetMetadataCache:
            table = duckdb_conn.get_table(datasetName)

            col = table[columnName]

            if tokenType == "word":
                word_tokens = word_tokenize.get_word_tokens_batch(col)
            else:
                word_tokens = word_tokenize.get_byte_encoding_batch(col)

            # TODO load word_tokens into duckdb table

            return DatasetTokenizeResponse(
                success=True, message="Dataset tokenized successfully."
            )

        return DatasetTokenizeResponse(
            success=False,
            message=f"Failed to tokenize, unkown dataset: {datasetName}.",
        )

    @api_app.get("/query_embed_from_id", response_model=VectorSearchResponse)
    async def query_embed_from_id(datasetName: str, id: int):
        vector = vectordb_conn.get_embedding_from_id(datasetName, id)
        result_df = vectordb_conn.search(datasetName, vector)
        return VectorSearchResponse(
            success=True, result=result_df.to_dict(orient="records")
        )

    @api_app.get("/query_embed_from_string", response_model=VectorSearchResponse)
    async def query_embed_from_string(datasetName: str, queryString: str):
        vector = vectordb_conn.get_embedding_from_string(datasetName, queryString)
        result_df = vectordb_conn.search(datasetName, vector)
        return VectorSearchResponse(
            success=True, result=result_df.to_dict(orient="records")
        )

    @api_app.post("/fetch_llm_response_format", response_model=LLMResponse)
    def get_llm_response_format(userPrompt: str):
        task_format = llm_client.get_response_format(userPrompt)
        return LLMResponse(success=True, result=task_format)

    @api_app.post("/fetch_llm_transform_result", response_model=LLMResponse)
    def get_llm_transform_result(request: LLMTransformRequest):
        results = llm_client.get_transformations(
            request.userPrompt,
            request.taskFormat,
            request.columnData,
            request.exampleData,
            request.exampleResponse,
        )
        print("[get_llm_transform_result] has results: ", results)
        return LLMResponse(success=True, result=results)

    @api_app.post("/commit_llm_transform_result", response_model=LLMResponse)
    def commit_llm_transform_result(request: LLMTransformCommit):

        print("Request is: ", request)

        all_data_df = duckdb_conn.connection.execute(
            f'SELECT "id", "{request.columnName}" from "{request.tableName}"'
        ).df()

        transform_data = pd.merge(
            all_data_df, pd.DataFrame({"id": request.applyToIndices}), on="id"
        )
        print("Transform data is: ", transform_data.head())

        # get results and turn into flat array
        results = llm_client.get_transformations(
            request.userPrompt,
            request.taskFormat,
            transform_data[request.columnName],
            request.exampleData,
            request.exampleResponse,
        )
        print("RAW RESULTS ARE: ", results)
        processed_results = process_results(results, request.newColumnName)
        processed_df = pd.DataFrame(
            {"processed": processed_results}, index=request.applyToIndices
        )
        processed_df = processed_df.reindex(all_data_df.index)
        print("processed_df: ", processed_df)

        # NOTE: assuming that this is unique col name
        new_col_name = "MODEL_" + request.newColumnName
        duckdb_conn.add_column(
            request.tableName, new_col_name, processed_df["processed"]
        )
        colType = get_type_from_response(request.taskFormat.type)
        datasetMetadataCache[request.tableName].columns.insert(
            0,
            Column(
                name=new_col_name,
                type=colType,
                derived_from=request.columnName,
                derived_how="model",
            ),
        )

        return LLMResponse(success=True, result=[])

    @api_app.post("/save_to_file", response_model=bool)
    def save_database_to_file(table_name: str):

        current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        file_path = f"{table_name}_{current_time}.parquet"

        duckdb_conn.write_table_to_file(table_name, file_path)

        return True

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
