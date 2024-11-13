import uvicorn
from typing import Dict, Callable, Optional
import multiprocess
import pandas as pd

from texture.models import DatasetInfo, DataType
from texture.server import get_server
from texture.utils import is_notebook
from texture.database.preprocess import validate_and_construct_tables

TEXTURE_SERVER_PROCESS = None

try:
    multiprocess.set_start_method("spawn", force=True)
except RuntimeError as e:
    print("RuntimeError: ", e)
    pass


def run(
    data: pd.DataFrame,
    column_overrides: Dict[str, DataType] = None,
    host: str = "localhost",
    port: int = 8080,
    api_key: str = None,
    create_new_embedding_func: Optional[Callable] = None,
):
    dataset_schema, load_tables = validate_and_construct_tables(data, column_overrides)

    if is_notebook():
        global TEXTURE_SERVER_PROCESS
        if TEXTURE_SERVER_PROCESS is not None:
            print("Terminating existing server process")
            TEXTURE_SERVER_PROCESS.terminate()
            TEXTURE_SERVER_PROCESS.join()

        print("Running from a notebook, starting a new process")

        TEXTURE_SERVER_PROCESS = multiprocess.Process(
            target=run_server,
            args=(
                dataset_schema,
                load_tables,
                api_key,
                host,
                port,
                create_new_embedding_func,
            ),
        )
        TEXTURE_SERVER_PROCESS.start()
        # below will block notebook from progressing past server cell
        # TEXTURE_SERVER_PROCESS.join()
    else:
        run_server(
            dataset_schema,
            load_tables,
            api_key,
            host,
            port,
            create_new_embedding_func,
        )


def run_server(
    dataset_schema: DatasetInfo,
    load_tables: Dict[str, pd.DataFrame],
    api_key: Optional[str] = None,
    host: Optional[str] = "localhost",
    port: Optional[int] = 8080,
    create_new_embedding_func: Optional[Callable] = None,
):

    app = get_server(
        dataset_schema,
        load_tables,
        create_new_embedding_func,
        api_key,
    )

    print(f"\n\033[1mTexture\033[0m running on http://{host}:{port}\n")
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="warning",  # info or warning
        # reload=True,
    )
