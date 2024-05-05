import uvicorn
from typing import Dict, Union, Any, List
from multiprocessing import Process
import torch
import numpy as np
import pandas as pd

from texture.models import (
    TextureInitArgs,
    DatasetInfo,
    DatasetInitArgs,
    ColumnInputTable,
)
from texture.server import get_server
from texture.utils import is_notebook
from texture import preprocess
import random

TEXTURE_SERVER_PROCESS = None


def run(
    data: pd.DataFrame,
    name: str = None,
    embeddings: Any = None,
    primary_key: str = None,
    column_tables: List[ColumnInputTable] = None,
    host: str = "localhost",
    port: int = 8080,
    load_example_data: bool = False,
):
    args = TextureInitArgs(
        data=data,
        name=name,
        embeddings=embeddings,
        primary_key=primary_key,
        column_tables=column_tables,
        host=host,
        port=port,
        load_example_data=load_example_data,
    )

    if is_notebook():
        print("Running from a notebook, starting a new process")

        global TEXTURE_SERVER_PROCESS
        if TEXTURE_SERVER_PROCESS is not None:
            TEXTURE_SERVER_PROCESS.terminate()

        TEXTURE_SERVER_PROCESS = Process(
            target=run_server,
            args=(args,),
        )
        TEXTURE_SERVER_PROCESS.start()
        # below will block notebook from progressing past server cell
        # TEXTURE_SERVER_PROCESS.join()
    else:
        run_server(args)


def run_server(args: Union[TextureInitArgs, Dict]):
    args = TextureInitArgs(**args) if isinstance(args, dict) else args

    dsInfo, load_tables, load_embeddings = validate_and_run_preprocess(args)

    app = get_server(
        DatasetInitArgs(
            datasetInfo=dsInfo, load_tables=load_tables, load_embeddings=load_embeddings
        ),
        load_example_data=args.load_example_data,
    )

    print(f"\n\033[1mTexture\033[0m running on http://{args.host}:{args.port}\n")
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        log_level="info",
        # reload=True,
    )


def validate_and_run_preprocess(args: TextureInitArgs):  # -> (DatasetInfo, Dict)
    df = args.data
    name = args.name
    sanitized_embeddings = None
    has_embeddings = False
    has_projection = False

    if not name:
        name = "dataset_" + str(random.randint(1000, 9999))

    inferred_data_types = preprocess.get_data_types(df)
    print("Inferred data types:", inferred_data_types)

    # make primary key if none provided (if provided make sure is unique)
    pk_name = args.primary_key
    if not (pk_name and pk_name in df.columns and df[pk_name].is_unique):
        if "id" in df.columns and df["id"].is_unique:
            pk_name = "id"
        else:
            print("No valid primary key found, creating a new one...")
            df = df.reset_index(drop=True)
            df = df.reset_index().rename(columns={"index": "id"})
            pk_name = "id"
            inferred_data_types.append({"name": pk_name, "type": "number"})

    # check if embeddings
    if args.embeddings is not None:

        sanitized_embeddings = verify_embeddings(args.embeddings)
        has_embeddings = True

        if not ("umap_x" in df.columns and "umap_y" in df.columns):
            print(
                "Did not find projection included (no umap_x, umap_y columns), calculating now..."
            )
            projection = preprocess.get_projection(sanitized_embeddings)

            df["umap_x"] = projection[:, 0]
            df["umap_y"] = projection[:, 1]
            has_projection = True

    # or just projection of embeddings
    if "umap_x" in df.columns and "umap_y" in df.columns:
        has_projection = True

    # validate that the column tables correspond to real columns
    if args.column_tables:
        for colTableInfo in args.column_tables:
            cols = colTableInfo.table_data.columns

            if pk_name not in cols:
                raise ValueError(
                    f"Primary key {pk_name} not found in column table:", colTableInfo
                )
            if colTableInfo.name not in cols:
                raise ValueError(
                    f"Column name {colTableInfo.name} not found in column table:",
                    colTableInfo,
                )

            # TODO: check if span_start and span_end are in columns maybe

    # populate dataset Info
    dsInfo, load_tables = create_ds_info(
        name,
        inferred_data_types,
        pk_name,
        args.column_tables,
        has_embeddings,
        has_projection,
    )
    load_tables[name] = df
    load_embeddings = None
    if sanitized_embeddings is not None:
        load_embeddings = {name: sanitized_embeddings}

    print("Created DS_INFO:", dsInfo)
    print("Created Load Tables:", load_tables)
    print("Created Load embeddings:", load_embeddings)

    return dsInfo, load_tables, load_embeddings


def verify_embeddings(e) -> np.ndarray:
    if isinstance(e, np.ndarray):
        return e
    if isinstance(e, torch.Tensor):
        return e.cpu().numpy()

    raise ValueError(
        "Embeddings must be a numpy.ndarray or torch.Tensor. Received: ", type(e)
    )


def create_ds_info(
    name, inferred_data_types, pk_name, column_tables, has_embeddings, has_projection
):

    pk_info = next(
        (entry for entry in inferred_data_types if entry["name"] == pk_name),
        {"name": pk_name, "type": "number"},  # backup if not found
    )

    derived_cols = []
    load_tables = {}
    if column_tables:
        for colTableInfo in column_tables:

            table_name = f"{colTableInfo.name}_{colTableInfo.derived_from}"  # hopefully this is unique
            load_tables[table_name] = colTableInfo.table_data

            derived_cols.append(
                {
                    "name": colTableInfo.name,
                    "type": "categorical",  # is this accurate?
                    "derived_from": colTableInfo.derived_from,
                    "table_name": table_name,
                }
            )

    return (
        DatasetInfo(
            name=name,
            primary_key=pk_info,
            origin="uploaded",
            columns=[*derived_cols, *inferred_data_types],
            has_embeddings=has_embeddings,
            has_projection=has_projection,
        ),
        load_tables,
    )
