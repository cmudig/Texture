# Dev loop for python package `texturebackend`

The backend hosts a FastAPI server and data processing functions along with the in process duckdb database for storing and filtering data.

## First time

Pre-requisites

1. Install conda
2. Install poetry

Make a new conda environment, can be called whatever

```bash
conda create -n texture python=3.10 # python 3.10 recommended for some package compatability
```

Installs dependencies AND builds in dev mode in current conda env

```bash
poetry install
```

## Backend dev loop

To start server:

```bash
cd texturebackend
uvicorn --factory server:get_server --reload
```

If you add a new python package, do it with poetry since will also install in current conda env with `poetry add name`.

If you add a new route or model to the backend, you can re-generate the api client in the frontend automatically (server must be running when this happens!).

```bash
cd texturefrontend
npm run gen-api
```

**NOTE:** be careful about what files get changed since some like the request handling and some types are manually edited. The following files should probably NOT be changed:

- `texturefrontend/src/backendapi/core/request.ts`: manual changes made to process blobs
- `texturefrontend/src/backendapi/models/ErrorResponse.ts`: changed type to not be any
- `texturefrontend/src/backendapi/models/ExecResponse.ts`: changed type to not be any
- `texturefrontend/src/backendapi/models/JsonResponse.ts`: changed type to not be any

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

# Dev loop for UI `texturefrontend`

The frontend is a svelte / vite app that uses the generated api client to communicate with the backend.

## First time

Pre-requisites

1. install node / npm

First time

```bash
cd texturefrontend
npm install # install packages
```

## Dev loop

Will start local server and hot re-load changes

```bash
cd texturefrontend
npm run dev
```

## Deploy

Deploy the built frontend to the `gh-pages` branch. Is served at [https://dig.cmu.edu/Texture/](https://dig.cmu.edu/Texture/).

```bash
npm run build
# npm run preview # preview the built version locally
npm run deploy
```

In the future, this can be done with a github action but right now we have dependencies on our mosaic mod so easier to build locally then just upload the result.

# Notes

- Right now manually linking mosaic (all packages) in `package.json` but can only do one install later
- IMPORTANT: need to have an envionment vaiable `OPENAI_API_KEY` set to use the openai api in the python environment
