import anywidget
import pandas as pd

import pathlib
from texture.runner import run


class TextureWidget(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "index.js"
    _css = pathlib.Path(__file__).parent / "index.css"

    def __init__(
        self,
        data: pd.DataFrame,
        launch_server: bool = True,
        *args,
        **kwargs,
    ):
        """Create a widget.

        Args:
            data (pd.DataFrame): the data to put into Texture
        """
        super().__init__(*args, **kwargs)
        if launch_server:
            self.run_server_process(data)

    def run_server_process(self, data):
        run(data)
