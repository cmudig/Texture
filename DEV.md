# Texture Development

Texture includes a python backend and a svelte frontend.

## First time

Pre-requisites:

1. Install conda
2. Install poetry (>=2.0.1)

Make a new conda environment

```bash
conda create -n texture python=3.12
```

Installs dependencies AND builds in dev mode in current conda env

```bash
poetry install
```

## Backend dev loop [`texture`](./texture/)

The backend is launched with the `texture.run()` command. This command will launch the backend server with a simple dataset.

```bash
python texture/runner_dev.py
```

Make sure to build frontend first or run a dev server or nothing will show up!

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
npm run dev
```

To see on same port as backend server, frontend must be built. The frontend build command outputs to [`texture/frontend/`](./texture/frontend/) but this folder is not git synced.

```bash
npm run build
```

## Docs

The docs are in a separate folder `/docs` and uses vitepress. Doc website is re-built on pushes to main. To run local doc server:

```bash
cd docs
npm run docs:dev
```

## Important Notes

- If you add a new python package, do it with poetry since will also install in current conda env with `poetry add name`.
- If you add a new route or model to the backend, you can re-generate the api client in the frontend automatically (server must be running when this happens!). This overwrites some files that we edited manually so be careful (this is why we have a rectify step): `npm run gen-api && npm run rectify-gen-api`
- Right now manually linking mosaic (all packages) in `package.json` but can only do one install later
- Need to have an envionment vaiable `OPENAI_API_KEY` set to use the openai api in the python environment

# Publish

First need to bump the version:

```bash
# bump version
poetry version patch
# commit version
git commit -am "chore: bump version to $(poetry version -s)"
# tag version
git tag "v$(poetry version -s)"
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
