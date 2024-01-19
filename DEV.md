# TL;DR

Terminal 1: Backend python server

```bash
cd textprofilerbackend
uvicorn --factory server:get_server --reload
```

Terminal 2: frontend svelte / vite UI

```bash
cd textprofilerfrontend
npm run dev
```

# Dev loop for python package `textprofilerbackend`

The backend hosts a FastAPI server and data processing functions along with the in process duckdb database for storing and filtering data.

## First time

Pre-requisites

1. Install conda
2. Install poetry

Make a new conda environment, can be called whatever

```bash
conda create -n text-profiler python=3.10 # python 3.10 recommended for some package compatability
```

Installs dependencies AND builds in dev mode in current conda env

```bash
poetry install
```

## Backend dev loop

To start server:

```bash
cd textprofilerbackend
uvicorn --factory server:get_server --reload
```

If you add a new python package, do it with poetry since will also install in current conda env with `poetry add name`.

If you add a new route or model to the backend, you can re-generate the api client in the frontend automatically (server must be running when this happens!).

```bash
cd textprofilerfrontend
npm run gen-api
```

**NOTE:** be careful about what files get changed since some like the request handling and some types are manually edited. The following files should probably NOT be changed:

- `textprofilerfrontend/src/backendapi/core/request.ts`: manual changes made to process blobs
- `textprofilerfrontend/src/backendapi/models/ErrorResponse.ts`: changed type to not be any
- `textprofilerfrontend/src/backendapi/models/ExecResponse.ts`: changed type to not be any
- `textprofilerfrontend/src/backendapi/models/JsonResponse.ts`: changed type to not be any

You can run the following commands to unset these files from git automatically after you regenerate the API (N.B this will remove other changes to these files):

```bash
npm run gen-api && npm run rectify-gen-api
```

## Release

To publish (only do this if you know you want to):

```bash
poetry build
poetry publish
```

This will install the python package in the current conda env so can be imported as:

```python
import textclean
```

# Dev loop for UI `textprofilerfrontend`

The frontend is a svelte / vite app that uses the generated api client to communicate with the backend.

## First time

Pre-requisites

1. install node / npm

First time

```bash
cd textprofilerfrontend
npm install # install packages
```

## Dev loop

Will start local server and hot re-load changes

```bash
cd textctextprofilerfrontendleanui
npm run dev
```
