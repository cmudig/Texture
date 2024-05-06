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

## Backend dev loop [`texture`](./texture/)

The backend can be run in two ways. We recommend running the uvicorn server directly for development since it has hot reloading and is faster. The `run_server` command is a wrapper around this runs the `texture.run()` command.

1. `uvicorn --factory texture.server:get_server --port 8080 --reload`
   OR
2. `poetry run run_server`

This will launch the server to whatever port is specified with the frontend hosted at the root and api. To launch the server. Be sure to build frontend first or nothing will show up!

Other notes:

- If you add a new python package, do it with poetry since will also install in current conda env with `poetry add name`.
- If you add a new route or model to the backend, you can re-generate the api client in the frontend automatically (server must be running when this happens!). This overwrites some files that we edited manually so be careful (this is why we have a rectify step): `npm run gen-api && npm run rectify-gen-api`

## Frontend dev loop [`texturefrontend`](./texturefrontend/)

The frontend is a svelte / vite app that uses the generated api client to communicate with the backend.

**First time**

```bash
cd texturefrontend
npm install
```

**Dev loop**

Will start local server and hot re-load changes. This will try to connect to the backend server at `localhost:8080` by default so make sure one of the server commands is running.

```bash
cd texturefrontend
npm run dev
```

To see on same port as backend server, frontend must be built. The frontend build command outputs to [`texture/frontend/`](./texture/frontend/) but this folder is not git synced.

```bash
npm run build
```

# Notes

- Right now manually linking mosaic (all packages) in `package.json` but can only do one install later
- IMPORTANT: need to have an envionment vaiable `OPENAI_API_KEY` set to use the openai api in the python environment

# Publish

First need to bump the version:

```bash
poetry version patch # bump version
git commit -am "chore: bump version to $(poetry version -s)" # commit version
git tag "v$(poetry version -s)" # tag version
```

Then build package:

```bash
# build frontend
cd texturefrontend
npm run build
# build python package
poetry build
```

Then release:

```bash
poetry publish
git push && git push --tags
```

After, create release on github.
