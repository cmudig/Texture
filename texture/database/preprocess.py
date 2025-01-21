import random
from typing import Dict, Tuple
import pandas as pd
import numpy as np

from texture.extra.embeddings import get_projection
from texture.models import DatasetSchema, Column, DataType
from texture.names import (
    C_VECTOR,
    C_EMBED_X,
    C_EMBED_Y,
    C_ID,
    C_SPAN_START,
    C_SPAN_END,
)


def preprocess(
    df: pd.DataFrame, column_type_overrides: Dict[str, DataType] = None
) -> Tuple[DatasetSchema, Dict[str, pd.DataFrame]]:
    has_embeddings = False
    has_projection = False
    name = "dataset_" + str(random.randint(100000, 999999))

    # make primary key if none provided (if provided make sure is unique)
    if not (C_ID in df.columns and df[C_ID].is_unique):
        df = df.reset_index(drop=True)
        df = df.reset_index().rename(columns={"index": C_ID})

    # check if embeddings
    if C_VECTOR in df.columns:
        has_embeddings = True

        if not (C_EMBED_X in df.columns and C_EMBED_Y in df.columns):
            print(
                f"Found '{C_VECTOR}' column but no projection (missing '{C_EMBED_X}', '{C_EMBED_Y}'). Projecting now..."
            )
            projection = get_projection(df[C_VECTOR])
            df[C_EMBED_X] = projection[:, 0]
            df[C_EMBED_Y] = projection[:, 1]

    # or just projection of embeddings
    if C_EMBED_X in df.columns and C_EMBED_Y in df.columns:
        has_projection = True

    pk_schema = Column(name=C_ID, type="number")
    column_schema, load_tables = construct_schema_and_tables(
        name, df, column_type_overrides
    )

    ds_info = DatasetSchema(
        name=name,
        primary_key=pk_schema,
        origin="uploaded",
        columns=column_schema,
        has_embeddings=has_embeddings,
        has_projection=has_projection,
    )

    return ds_info, load_tables


def construct_schema_and_tables(
    name: str,
    df: pd.DataFrame,
    column_type_overrides: Dict[str, DataType] = None,
):
    """
    Get the data types of each column in the DataFrame.
    Maps each column to a semantic type: 'number', 'date', 'text', or 'categorical'
    """
    schemas = []
    new_tables = {}

    for col_name, dtype in df.dtypes.items():
        # no schema for reserved columns since special handling
        if col_name in [C_VECTOR, C_EMBED_X, C_EMBED_Y, C_ID]:
            continue
        if column_type_overrides is not None and col_name in column_type_overrides:
            schemas.append(Column(name=col_name, type=column_type_overrides[col_name]))
        elif is_numeric(dtype):
            schemas.append(Column(name=col_name, type="number"))
        elif is_date(dtype):
            schemas.append(Column(name=col_name, type="date"))
        elif any(
            df[col_name].apply(lambda x: isinstance(x, (list, tuple, np.ndarray)))
        ):
            # is a list
            df_primed = df.set_index(C_ID)

            exploded = (
                df_primed[col_name]
                .explode()
                .reset_index()
                .rename(columns={"index": C_ID})
                .dropna(subset=[col_name])
            )

            # NOTE: assumed these are non-segment lists so the spans are array index
            exploded[C_SPAN_START] = exploded.groupby(C_ID).cumcount()
            exploded[C_SPAN_END] = exploded[C_SPAN_START] + 1

            # Save parsed column
            new_table_name = col_name + "_parsed"
            new_tables[new_table_name] = exploded

            # delete original list col
            df = df.drop(columns=[col_name])

            # get type
            parsed_type = "categorical"
            if is_numeric(exploded[col_name].dtype):
                parsed_type = "number"
            elif is_date(exploded[col_name].dtype):
                parsed_type = "date"

            parsed_schema = Column(
                name=col_name,
                type=parsed_type,
                derivedSchema={
                    "is_segment": False,
                    "table_name": new_table_name,
                    "derived_from": None,  # since non-segment leave as None
                    "derived_how": None,
                },
            )

            schemas.append(parsed_schema)

        else:
            max_col_len = df[col_name].str.len().max()
            cardinality = df[col_name].nunique()

            # heuristic to detect text or categorical
            if (max_col_len > 200) or (cardinality == len(df)):
                estimated_type = "text"
            else:
                estimated_type = "categorical"

            c = Column(name=col_name, type=estimated_type)
            schemas.append(c)

    new_tables[name] = df

    return schemas, new_tables


def is_numeric(type) -> bool:
    return pd.api.types.is_numeric_dtype(type)


def is_date(type) -> bool:
    return pd.api.types.is_datetime64_any_dtype(type)
