# Texture: Structured Text Analytics

[![PyPi](https://img.shields.io/pypi/v/texture-viz.svg)](https://pypi.org/project/texture-viz/)

Texture is a system for exploring and creating structured insights with your text datasets.

1. **Interactive Attribute Profiles**: Texture visualizes structured attributes alongside your text data in interactive, cross-filterable charts.
2. **Flexible attribute definitions**: Attribute charts can come from different tables and any level of a document such as words, sentences, or documents.
3. **Embedding based operations**: Texture helps you use vector embeddings to search for similar text and summarize your data.

![screenshot of Texture interface](.github/screenshots/texture_sc.png)

## Install and run

Install texture with pip:

```bash
pip install texture-viz
```

Then you can run in a python script or notebook by providing a dataframe with your text data and attributes.

```python
import texture
texture.run(df)
```

## Texture Docs

Texture allows you to customize attribute visualizations based on a schema and configure different tables to tailor how the interface presents your data. For more details and examples, check out our [documentation](https://dig.cmu.edu/Texture/).

## Dev install

See [DEV.md](DEV.md) for dev workflows and setup.
