from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from typing import Dict, Callable, Optional
import os
import pandas as pd
from datetime import datetime
from texture.database.connection import initialize_databases
from texture.models import (
    DatasetSchema,
    DuckQueryData,
    DuckQueryResult,
    TransformResponse,
    LLMTransformRequest,
    LLMTransformCommit,
    Column,
    CodeTransformRequest,
    CodeTransformCommit,
    DerivedSchema,
)
from texture.userTransformLLM.client import LLMClient
from texture.utils import get_type_from_response, flatten
from texture.userTransformCode.transform import (
    execute_code_and_apply_function,
)


def custom_generate_unique_id(route: APIRoute):
    """
    Replaces default generated name for TS objects with camel-cased method name.
    So python function `read_item` -> readItem
    NOTE: must ensure that route names are unique or will cause issues!
    """
    return route.name


class Counter:
    def __init__(self):
        self.counter = 0

    def increment(self):
        self.counter += 1
        return self.counter

    def get(self):
        return self.counter


def get_server(
    schema: DatasetSchema,
    load_tables: Dict[str, pd.DataFrame],
    create_new_embedding_func: Optional[Callable] = None,
    api_key: str = None,
) -> FastAPI:
    ### Database set up
    duckdb_conn, vectordb_conn = initialize_databases(
        schema, load_tables, create_new_embedding_func
    )
    llm_client = LLMClient(api_key=api_key)

    ### state tracking
    embed_query_counter = Counter()

    ### Web server set up
    app = FastAPI(
        title="Texture server",
    )

    # TODO: use env variables in future for this?
    origins = [
        "http://localhost:5173",  # default vite dev
        "http://localhost:4173",  # default vite preview
        "https://dig.cmu.edu",  # deployed url
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api_app = FastAPI(
        title="Texture Backend API",
        generate_unique_id_function=custom_generate_unique_id,
        # TODO: unsure if this is necessary...
        default_response_class=ORJSONResponse,
    )

    app.mount("/api", api_app)

    app.mount(
        "/",
        StaticFiles(
            directory=os.path.dirname(os.path.realpath(__file__)) + "/frontend",
            html=True,
        ),
        name="base",
    )

    @api_app.get(
        "/status",
        response_model=str,
    )
    def root_status():
        return "hello from backend server"

    @api_app.get(
        "/get_dataset_schema",
        response_model=DatasetSchema,
    )
    def read_dataset_info():
        """
        Get the datasets available along with a summary of their columns
        """

        return schema

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

    @api_app.get("/run_embed_search", response_model=Column)
    async def run_embed_search(tableName: str, id: int = None, queryString: str = None):
        if id is None and queryString is None:
            raise ValueError("Must provide either id or queryString")

        if id is not None:
            vector = vectordb_conn.get_embedding_from_id(tableName, id)
        else:
            vector = vectordb_conn.get_embedding_from_string(tableName, queryString)

        # local vars
        new_col_name = "similarity_search_result"
        embed_query_counter.increment()
        id_col_name = schema.primary_key.name

        # pd.Dataframe with [id, _distance] columns
        result_df = vectordb_conn.search(tableName, vector)
        result_df = result_df.rename(columns={"_distance": new_col_name})

        # make sure indices align
        df_ids = duckdb_conn.connection.execute(
            f'SELECT "{id_col_name}" from "{tableName}"'
        ).df()

        merged_df = pd.merge(df_ids, result_df, on="id")
        duckdb_conn.add_column(tableName, new_col_name, merged_df[new_col_name])

        newColSchema = Column(
            name=new_col_name,
            type="number",
            extra={
                "search_id": id,
                "search_query": queryString,
            },
        )

        if schema.search_result is not None:
            # remove old search result from cols
            schema.columns = [
                col for col in schema.columns if col.name != schema.search_result.name
            ]

        schema.columns.insert(0, newColSchema)
        schema.search_result = newColSchema

        return newColSchema

    @api_app.post("/fetch_llm_response_format", response_model=TransformResponse)
    def get_llm_response_format(userPrompt: str):
        try:
            task_format = llm_client.get_response_format(userPrompt)
            return TransformResponse(success=True, result=task_format)
        except Exception as e:
            print("Error in /fetch_llm_response_format::: ", str(e))
            return TransformResponse(success=False, result={"error": str(e)})

    @api_app.post("/fetch_llm_transform_result", response_model=TransformResponse)
    def get_llm_transform_result(request: LLMTransformRequest):
        try:
            results = llm_client.get_transformations(
                request.userPrompt,
                request.taskFormat,
                request.columnData,
                request.exampleData,
                request.exampleResponse,
            )
            parsed_results = [r[request.taskFormat.name] for r in results]
            return TransformResponse(success=True, result=parsed_results)
        except Exception as e:
            print("ERROR in /fetch_llm_transform_result ", str(e))
            return TransformResponse(success=False, result={"error": str(e)})

    @api_app.post("/commit_llm_transform_result", response_model=TransformResponse)
    def commit_llm_transform_result(request: LLMTransformCommit):
        try:
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
                    derivedSchema=DerivedSchema(
                        is_segment=False,
                        table_name=newTableName,
                        derived_from=request.columnName,
                        derived_how="model",
                    ),
                )
            else:
                if colType == "number":
                    processed_df[new_col_name] = pd.to_numeric(
                        processed_df[new_col_name]
                    )

                all_merged = pd.merge(all_data_df, processed_df, on="id", how="left")

                duckdb_conn.add_column(
                    request.tableName, new_col_name, all_merged[new_col_name]
                )
                newColSchema = Column(
                    name=new_col_name,
                    type=colType,
                    derivedSchema=DerivedSchema(
                        is_segment=False,
                        table_name=newTableName,
                        derived_from=request.columnName,
                        derived_how="model",
                    ),
                )

            schema.columns.insert(0, newColSchema)

            return TransformResponse(success=True, result=[])

        except Exception as e:
            print("Error in /commit_llm_transform_result::: ", str(e))
            return TransformResponse(success=False, result={"error": str(e)})

    @api_app.post("/fetch_code_transform_result", response_model=TransformResponse)
    def get_code_transform_result(request: CodeTransformRequest):
        try:
            df = pd.DataFrame({"sample": request.columnData})
            results = execute_code_and_apply_function(request.codeString, df["sample"])
            if results is None:
                raise Exception("No results returned from code execution")

            return TransformResponse(success=True, result=list(results))

        except Exception as e:
            print("Exception running user code: ", e)
            return TransformResponse(success=False, result={"error": str(e)})

    @api_app.post("/commit_code_transform_result", response_model=TransformResponse)
    def commit_code_transform_result(request: CodeTransformCommit):
        new_col_name = request.taskFormat.name

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
                derivedSchema=DerivedSchema(
                    is_segment=False,
                    table_name=newTableName,
                    derived_from=request.columnName,
                    derived_how="code",
                ),
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
                derivedSchema=DerivedSchema(
                    is_segment=False,
                    table_name=newTableName,
                    derived_from=request.columnName,
                    derived_how="code",
                ),
            )

        schema.columns.insert(0, newColSchema)
        return TransformResponse(success=True, result=[])

    @api_app.post("/save_to_file", response_model=bool)
    def save_database_to_file(table_name: str):
        all_table_names = set([table_name])
        # get all table names
        for col in schema.columns:
            if col.table_name is not None:
                all_table_names.add(col.table_name)

        print("Saving tables: ", all_table_names)

        for t_name in all_table_names:
            current_time = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
            file_path = f"{t_name}_{current_time}.parquet"
            duckdb_conn.write_table_to_file(t_name, file_path)

        return True

    return app
