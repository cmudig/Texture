from fastapi import FastAPI, UploadFile, File
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from typing import Dict, Literal


from texturebackend.database import init_db
from texturebackend.models import (
    DatasetInfo,
    DuckQueryData,
    DuckQueryResult,
    DatasetUploadResponse,
    DatasetVerifyResponse,
    DatasetTokenizeResponse,
    VectorSearchResponse,
    TransformResponse,
    LLMTransformRequest,
    LLMTransformCommit,
    Column,
    CodeTransformRequest,
    CodeTransformCommit,
)
from texturebackend.process_data import process_new_file
from texturebackend.transform import word_tokenize
from texturebackend.llm.client import LLMClient
from texturebackend.utils import get_type_from_response, flatten
from texturebackend.userCodeTransform.transform import (
    execute_code_and_apply_function,
)

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

    @api_app.post("/fetch_llm_response_format", response_model=TransformResponse)
    def get_llm_response_format(userPrompt: str):
        task_format = llm_client.get_response_format(userPrompt)
        return TransformResponse(success=True, result=task_format)

    @api_app.post("/fetch_llm_transform_result", response_model=TransformResponse)
    def get_llm_transform_result(request: LLMTransformRequest):
        results = llm_client.get_transformations(
            request.userPrompt,
            request.taskFormat,
            request.columnData,
            request.exampleData,
            request.exampleResponse,
        )
        parsed_results = [r[request.taskFormat.name] for r in results]
        print("[get_llm_transform_result] has results: ", parsed_results)
        return TransformResponse(success=True, result=parsed_results)

    @api_app.post("/commit_llm_transform_result", response_model=TransformResponse)
    def commit_llm_transform_result(request: LLMTransformCommit):
        new_col_name = request.taskFormat.name

        # Step 1: get data
        all_data_df = duckdb_conn.connection.execute(
            f'SELECT "id", "{request.columnName}" from "{request.tableName}"'
        ).df()
        transform_data = pd.merge(
            all_data_df, pd.DataFrame({"id": request.applyToIndices}), on="id"
        )

        # Step 2: get results and turn into flat array
        results = llm_client.get_transformations(
            request.userPrompt,
            request.taskFormat,
            transform_data[request.columnName],
            request.exampleData,
            request.exampleResponse,
        )

        # Step 3: format with correct indices transform
        processed_results = [r[new_col_name] for r in results]
        processed_df = pd.DataFrame(
            {new_col_name: list(processed_results), "id": transform_data["id"]}
        )

        colType = get_type_from_response(request.taskFormat.type)

        if request.taskFormat.num_replies == "multiple":
            newTableDf = flatten(processed_df[new_col_name], idColName="id")
            if colType == "number":
                newTableDf[new_col_name] = pd.to_numeric(newTableDf[new_col_name])
            newTableName = new_col_name + "_table"
            duckdb_conn.load_dataframe(newTableName, newTableDf)
            newColSchema = Column(
                name=new_col_name,
                type=colType,
                table_name=newTableName,
                derived_from=request.columnName,
                derived_how="model",
            )
        else:
            if colType == "number":
                processed_df[new_col_name] = pd.to_numeric(processed_df[new_col_name])

            all_merged = pd.merge(all_data_df, processed_df, on="id", how="left")

            duckdb_conn.add_column(
                request.tableName, new_col_name, all_merged[new_col_name]
            )
            newColSchema = Column(
                name=new_col_name,
                type=colType,
                derived_from=request.columnName,
                derived_how="model",
            )

        datasetMetadataCache[request.tableName].columns.insert(0, newColSchema)

        return TransformResponse(success=True, result=[])

    @api_app.post("/fetch_code_transform_result", response_model=TransformResponse)
    def get_code_transform_result(request: CodeTransformRequest):

        df = pd.DataFrame({"sample": request.columnData})

        try:
            results = execute_code_and_apply_function(request.codeString, df["sample"])
            if results is None:
                raise Exception("No results returned from code execution")

        except Exception as e:
            print("Exception running user code: ", e)
            return TransformResponse(success=False, result={"error": str(e)})

        return TransformResponse(success=True, result=list(results))

    @api_app.post("/commit_code_transform_result", response_model=TransformResponse)
    def commit_code_transform_result(request: CodeTransformCommit):
        new_col_name = request.taskFormat.name

        print("request is: ", request)

        # Step 1: get data
        all_data_df = duckdb_conn.connection.execute(
            f'SELECT "id", "{request.columnName}" from "{request.tableName}"'
        ).df()
        transform_data = pd.merge(
            all_data_df, pd.DataFrame({"id": request.applyToIndices}), on="id"
        )

        # Step 2: do transform
        try:
            results = execute_code_and_apply_function(
                request.codeString, transform_data[request.columnName]
            )
            if results is None:
                raise Exception("No results returned from code execution")
        except Exception as e:
            print("Exception running user code: ", e)
            return TransformResponse(success=False, result={"error": str(e)})

        print("results are: ", results)

        # Step 3: format with correct indices transform
        processed_df = pd.DataFrame(
            {new_col_name: list(results), "id": transform_data["id"]}
        )
        colType = get_type_from_response(request.taskFormat.type)

        if request.taskFormat.num_replies == "multiple":
            newTableDf = flatten(processed_df[new_col_name], idColName="id")
            if colType == "number":
                newTableDf[new_col_name] = pd.to_numeric(newTableDf[new_col_name])
            newTableName = new_col_name + "_table"
            duckdb_conn.load_dataframe(newTableName, newTableDf)
            newColSchema = Column(
                name=new_col_name,
                type=colType,
                table_name=newTableName,
                derived_from=request.columnName,
                derived_how="code",
            )
        else:
            if colType == "number":
                processed_df[new_col_name] = pd.to_numeric(processed_df[new_col_name])

            all_merged = pd.merge(all_data_df, processed_df, on="id", how="left")

            duckdb_conn.add_column(
                request.tableName, new_col_name, all_merged[new_col_name]
            )
            newColSchema = Column(
                name=new_col_name,
                type=colType,
                derived_from=request.columnName,
                derived_how="code",
            )

        datasetMetadataCache[request.tableName].columns.insert(0, newColSchema)
        return TransformResponse(success=True, result=[])

    @api_app.post("/save_to_file", response_model=bool)
    def save_database_to_file(table_name: str):

        all_table_names = set([table_name])
        # get all table names
        for col in datasetMetadataCache[table_name].columns:
            if col.table_name is not None:
                all_table_names.add(col.table_name)

        print("Saving tables: ", all_table_names)

        for t_name in all_table_names:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
            file_path = f"{t_name}_{current_time}.parquet"
            duckdb_conn.write_table_to_file(t_name, file_path)

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
