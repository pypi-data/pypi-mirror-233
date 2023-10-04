import importlib.metadata
import pathlib

import anywidget
import pandas as pd
import traitlets

try:
    __version__ = importlib.metadata.version("canica")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


class CanicaTSNE(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = pathlib.Path(__file__).parent / "static" / "widget.css"

    # Data used by the widget
    data = traitlets.Dict().tag(sync=True)
    embedding_var_name = traitlets.Unicode().tag(sync=True)
    hue_var_name = traitlets.Unicode().tag(sync=True)

    def __init__(self, df: pd.DataFrame, embeddings: str, hue_var: str) -> None:
        """Create a new EmbeddingViewer widget.

        Args:
            df: DataFrame containing the text, embeddings, and hue_var
            embeddings: Name of the column containing the embeddings
            hue_var: Name of the column containing the variable to color by
        """
        super().__init__()

        assert isinstance(embeddings, str), "embeddings variable must be a string"
        assert isinstance(hue_var, str), "hue_var variable must be a string"

        self.embedding_var_name = embeddings
        self.hue_var_name = hue_var

        # Extract desired columns from DataFrame
        _text = df.text
        _hue = df[self.hue_var_name].astype(float)
        _embeddings = [emb.tolist() for emb in df[self.embedding_var_name]]

        # Build new DataFrame with desired columns, save as dict
        self.data = pd.DataFrame(
            {"text": _text, "hue_var": _hue, "embeddings": _embeddings},
            index=df.index,
        ).to_dict()
