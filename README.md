# Texture: Structured Text Analytics

Texture is a system for exploring and creating structured insights with your text datasets.

1. Texture visualizes structured attributes alongside your text datasets in interactive, cross-filterable charts.
2. Attribute charts can come from any level of a document such as words, sentences, or documents.
3. Texture helps you derive new attributes during analysis with code and LLM transformations.

![screenshot of Texture interface](.github/screenshots/texture_sc.png)

## Installation

Pip installation coming soon!

```python
import texture

texture.run(df) # launch texture app

```

## Dev install

tl;dr below, see [DEV.md](DEV.md) for more details about dev workflows and setup.

If using VSCode (recommended), launching the servers below is configured as a build task you can launch with `Cmd+Shift+P` > `Tasks: Run Build Task` > `Launch Texture`; otherwise you can launch manually:

Terminal 1: Backend python server

```bash
poetry run run_server
```

Terminal 2: frontend svelte UI

```bash
cd texturefrontend
npm run dev
```
