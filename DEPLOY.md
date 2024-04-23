To publish hosted versions of this project you need to publish both the frontend and python server.

# Deploy frontend

Deploy the built frontend to the `gh-pages` branch. Is served at [https://dig.cmu.edu/Texture/](https://dig.cmu.edu/Texture/).

```bash
npm run build
# npm run preview # preview the built version locally
npm run deploy
```

In the future, this can be done with a github action but right now we have dependencies on our mosaic mod so easier to build locally then just upload the result.

# Deploy backend

This is a little bit tricker since need to containerize the app then deploy to a hosted server like GCP.

Not putting exact steps to avoid putting GCP project ids in git, but to build docker image run the following from root:

```bash
docker build --build-arg OPENAI_API_KEY=$OPENAI_API_KEY -t texture .
```
