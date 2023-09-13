# Dev loop for python package `textclean`

Pre-requisites

1. Install conda
2. Install poetry

## First time

Make a new conda environment, can be called whatever

```bash
conda create -n text-clean python
```

## Dev loop

Installs dependencies AND builds in dev mode in current conda env

```bash
poetry install
```

publish (only do this if you know you want to)

```bash
poetry build
poetry publish
```

This will install the python package in the current conda env so can be imported as:

```python
import textclean
```

# Dev loop for UI `textcleanui`

Pre-requisites

1. install node / npm

## First time

First time

```bash
cd slicecompareui
npm install # install packages
```

## Dev loop

Will start local server and hot re-load changes

```bash
cd slicecompareui
npm run dev
```
