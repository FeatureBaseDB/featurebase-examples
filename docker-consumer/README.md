# Simple Docker Consumer
This example contains a Dockerfile and compose file to start a container to insert sample data into a containerized FeatureBase server. This example may be used with the [docker-simple](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/docker-simple) or [docker-cluster](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/docker-cluster) examples.

## Check Out the Repo
Clone the FeatureBase examples repo in a terminal and change into the `docker-simple` directory:

```
git clone https://github.com/FeatureBaseDB/featurebase-examples.git
cd featurebase-examples/docker-simple
```

## Create the Docker Network
Before starting the FeatureBase container(s), you will need to create a Docker network to be used by the services:

```
docker network create fbnet
```

**OUTPUT**:

```
kord@Bob docker-simple $ docker network create fbnet
25ef7ce6391b74842ee86f31eb1dd3ebe9abe1f29d7642a3570ce7c604eb91ae
```

## Start the Services
Start a FeatureBase instance the services using `docker-compose`:

```
docker compose up
```

**NOTE**: If you have issues with `docker compose`, try disabling v2 by going into *settings..general* in Docker Desktop.


## Run the Consumer Container
The `sample.csv` in the `featurebase-examples/docker-consumer` directory will be copied into the container and used to insert the data into FeatureBase via the CSV consumer:

```
cd ../docker-consumer/
docker compose up
```

**OUTPUT**:

```
⠿ Volume "docker-consumer_featurebase-consumer"  Created                                                          0.0s
⠿ Container docker-consumer-csv-consumer-1       Created                                                          0.8s
Attaching to docker-consumer-csv-consumer-1
docker-consumer-csv-consumer-1  | Molecula Consumer v3.30.0, build time 2023-02-01T21:19:58+0000
docker-consumer-csv-consumer-1  | 2023-02-01T22:53:27.730887Z INFO:  Serving Prometheus metrics with namespace "ingester_csv" at localhost:9093/metrics
docker-consumer-csv-consumer-1  | 2023-02-01T22:53:27.739919Z INFO:  Listening for /debug/pprof/ and /debug/fgprof on 'localhost:6062'
docker-consumer-csv-consumer-1  | 2023-02-01T22:53:27.780440Z INFO:  start ingester 0
docker-consumer-csv-consumer-1  | 2023-02-01T22:53:27.784378Z INFO:  processFile: /featurebase/sample.csv
docker-consumer-csv-consumer-1  | 2023-02-01T22:53:27.788048Z INFO:  new schema: []idk.Field{idk.IDField{NameVal:"id", DestNameVal:"id", Mutex:false, Quantum:"", TTL:"", CacheConfig:(*idk.CacheConfig)(nil)}, idk.StringArrayField{NameVal:"draw", DestNameVal:"draw", Quantum:"", TTL:"", CacheConfig:(*idk.CacheConfig)(nil)}, idk.IDField{NameVal:"draw_size", DestNameVal:"draw_size", Mutex:false, Quantum:"", TTL:"", CacheConfig:(*idk.CacheConfig)(nil)}}
docker-consumer-csv-consumer-1  | 2023-02-01T22:53:27.837135Z INFO:  translating batch of 9 took: 10.757166ms
docker-consumer-csv-consumer-1  | 2023-02-01T22:53:27.838490Z INFO:  making fragments for batch of 9 took 1.522584ms
docker-consumer-csv-consumer-1  | 2023-02-01T22:53:27.948296Z INFO:  importing fragments took 109.795833ms
docker-consumer-csv-consumer-1  | 2023-02-01T22:53:27.950797Z INFO:  1 records processed 0-> (10)
docker-consumer-csv-consumer-1  | 2023-02-01T22:53:27.950963Z INFO:  metrics: import=131.721333ms
```

**NOTE**:
If you want to add to or update the CSV file, run these two commands first:

```
docker container prune
docker volume rm docker-consumer_featurebase-consumer
```

Restart the container to insert the new file:

```
docker compose up
```