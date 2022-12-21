# Simple Docker Consumer
This example contains a Dockerfile and compose file to start a container to insert sample data into a containerized FeatureBase server. This example may be used with the [docker-simple](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/docker-simple) or [docker-cluster](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/docker-cluster) examples.

## Check Out the Repo
Clone the FeatureBase examples repo in a terminal and change into the `docker-simple` directory:

```
git clone https://github.com/FeatureBaseDB/featurebase-examples.git
cd featurebase-examples/docker-simple
```

## Start the Services
Start the services using `docker-compose`:

```
docker-compose up -d
```

**NOTE**: If you have issues with `docker compose`, try disabling v2 by going into *settings..general* in Docker Desktop.

You should now have a container running:

![screenshot](container.png)

