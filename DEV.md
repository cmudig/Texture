# TL;DR

Terminal 1:

```bash
cd textclean
poetry install
```

Terminal 2:

```bash
cd textcleanui
npm run dev
```

# Dev loop for python package `textclean`

## First time

Pre-requisites

1. Install conda
2. Install poetry

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

## First time

Pre-requisites

1. install node / npm

First time

```bash
cd textcleanui
npm install # install packages
```

## Dev loop

Will start local server and hot re-load changes

```bash
cd textcleanui
npm run dev
```

## server

Run server

```bash
cd backend
uvicorn --factory server:get_server --reload
```

When add or edit a route, go to frontend and re-generate the api client (server must be running when this happens!).

This will generate the ts code in `src/backendapi`

```bash
cd textcleanui
npm run gen-api
```
