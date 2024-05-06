# Texture: Structured Text Analytics

[![PyPi](https://img.shields.io/pypi/v/texture-viz.svg)](https://pypi.org/project/texture-viz/)

Texture is a system for exploring and creating structured insights with your text datasets.

1. Texture visualizes structured attributes alongside your text datasets in interactive, cross-filterable charts.
2. Attribute charts can come from any level of a document such as words, sentences, or documents.
3. Texture helps you derive new attributes during analysis with code and LLM transformations.

![screenshot of Texture interface](.github/screenshots/texture_sc.png)

## Install and run

Install texture with pip:

```bash
pip install texture-viz
```

Then you can run in a python script or notebook. The run command takes in a pandas dataframe with a text column and optional metadata columns:

```python
import texture

texture.run(df) # launch texture app

```

## Dev install

See [DEV.md](DEV.md) for dev workflows and setup.
