import random
import torch
import numpy as np
from typing import List

from texture import preprocess
from texture.models import TextureInitArgs, DatasetInfo, Column, ColumnInputInfo


def validate_and_run_preprocess(args: TextureInitArgs):
    df = args.data
    name = args.name
    column_info = args.column_info
    sanitized_embeddings = None
    has_embeddings = False
    has_projection = False

    if not name:
        name = "dataset_" + str(random.randint(1000, 9999))

    if not column_info:
        column_info = preprocess.get_data_types(df)

    # make primary key if none provided (if provided make sure is unique)
    pk_name = args.primary_key
    if not (pk_name and pk_name in df.columns and df[pk_name].is_unique):
        if "id" in df.columns and df["id"].is_unique:
            pk_name = "id"
        else:
            # print("No valid primary key found, creating a new one...")
            df = df.reset_index(drop=True)
            df = df.reset_index().rename(columns={"index": "id"})
            pk_name = "id"
            column_info.append(ColumnInputInfo(name=pk_name, type="number"))

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

    # populate dataset Info
    dsInfo, load_tables = create_ds_info(
        name,
        column_info,
        pk_name,
        has_embeddings,
        has_projection,
    )
    load_tables[name] = df
    load_embeddings = None
    if sanitized_embeddings is not None:
        load_embeddings = {name: sanitized_embeddings}

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
    name: str,
    column_info: List[ColumnInputInfo],
    pk_name: str,
    has_embeddings: bool,
    has_projection: bool,
):

    pk_info = Column(name=pk_name, type="number")  # backup if not found

    cleaned_cols = []
    load_tables = {}

    for c_info in column_info:
        if c_info.name == pk_name:
            pk_info = c_info

        if c_info.table_name is not None and c_info.table_data is None:
            raise ValueError(f"Column {c_info.name} has table_name but no table_data")

        table_name = None
        if c_info.table_data is not None:

            # validate the passsed dataframe
            cols = c_info.table_data.columns
            if pk_name not in cols:
                raise ValueError(
                    f"Primary key {pk_name} not found in column table:", c_info
                )
            if c_info.name not in cols:
                raise ValueError(
                    f"Column name {c_info.name} not found in column table:",
                    c_info,
                )

            # TODO: check if span_start and span_end are in columns maybe

            if c_info.table_name:
                table_name = c_info.table_name
            else:
                table_name = f"{c_info.name}_{c_info.derived_from}"

            load_tables[table_name] = c_info.table_data

        # make Column without table_data from ColumnInputInfo
        c = Column(
            name=c_info.name,
            type=c_info.type,
            derived_from=c_info.derived_from,
            table_name=table_name,
            derived_how=c_info.derived_how,
        )

        cleaned_cols.append(c)

    return (
        DatasetInfo(
            name=name,
            primary_key=pk_info,
            origin="uploaded",
            columns=cleaned_cols,
            has_embeddings=has_embeddings,
            has_projection=has_projection,
        ),
        load_tables,
    )
