import uvicorn
from typing import Dict, Union, Any, List
from multiprocessing import Process
import pandas as pd

from texture.models import (
    TextureInitArgs,
    DatasetInitArgs,
    ColumnInputInfo,
)
from texture.server import get_server
from texture.utils import is_notebook
from texture import preprocess

TEXTURE_SERVER_PROCESS = None


def run(
    data: pd.DataFrame,
    name: str = None,
    embeddings: Any = None,
    primary_key: str = None,
    column_info: List[ColumnInputInfo] = None,
    host: str = "localhost",
    port: int = 8080,
    load_example_data: bool = False,
    api_key: str = None,
):
    args = TextureInitArgs(
        data=data,
        name=name,
        embeddings=embeddings,
        primary_key=primary_key,
        column_info=column_info,
        host=host,
        port=port,
        load_example_data=load_example_data,
        api_key=api_key,
    )

    if is_notebook():
        print("Running from a notebook, starting a new process")

        global TEXTURE_SERVER_PROCESS
        if TEXTURE_SERVER_PROCESS is not None:
            print("Terminating existing server process")
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

    dsInfo, load_tables, load_embeddings = preprocess.validate_and_run_preprocess(args)

    app = get_server(
        DatasetInitArgs(
            datasetInfo=dsInfo, load_tables=load_tables, load_embeddings=load_embeddings
        ),
        load_example_data=args.load_example_data,
        api_key=args.api_key,
    )

    print(f"\n\033[1mTexture\033[0m running on http://{args.host}:{args.port}\n")
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        log_level="warning",
        # reload=True,
    )
