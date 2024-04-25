import uvicorn
from typing import Dict, Union
from multiprocessing import Process

from texture.models import TextureInitArgs
from texture.server import get_server

TEXTURE_SERVER_PROCESS = None


def run(args: Union[TextureInitArgs, Dict]):

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
    # TODO process data if necessary
    args = TextureInitArgs(**args) if isinstance(args, dict) else args

    app = get_server()

    print(
        f"\n\033[1mTexture\033[0m running on http://{args.host}:{args.frontend_port}\n"
    )
    uvicorn.run(app, host=args.host, port=args.frontend_port, log_level="info")


def is_notebook() -> bool:
    try:
        from IPython.core.getipython import get_ipython

        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except (NameError, ImportError):
        return False  # Probably standard Python interpreter
