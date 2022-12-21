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
Start the services using `docker-compose`:

```
docker compose up
```

**NOTE**: If you have issues with `docker compose`, try disabling v2 by going into *settings..general* in Docker Desktop.


## Run the Consumer Container
The `sample.csv` will be copied into the container and then used to insert the data into FeatureBase using the CSV consumer:

```
docker compose up
```

**OUTPUT**:

```
 ⠿ Volume "docker-consumer_featurebase-consumer"  Created                                                          0.0s
 ⠿ Container docker-consumer-csv-consumer-1       Created                                                          0.8s
Attaching to docker-consumer-csv-consumer-1
docker-consumer-csv-consumer-1  | Molecula Consumer v3.26.0-9-g14f19300, build time 2022-12-12T20:47:21+0000
docker-consumer-csv-consumer-1  | 2022-12-21T22:23:40.092373Z INFO:  Serving Prometheus metrics with namespace "ingester_csv" at localhost:9093/metrics
docker-consumer-csv-consumer-1  | 2022-12-21T22:23:40.097076Z INFO:  Listening for /debug/pprof/ and /debug/fgprof on 'localhost:6062'
docker-consumer-csv-consumer-1  | 2022-12-21T22:23:40.157372Z INFO:  start ingester 0
docker-consumer-csv-consumer-1  | 2022-12-21T22:23:40.161222Z INFO:  processFile: /featurebase/sample.csv
docker-consumer-csv-consumer-1  | 2022-12-21T22:23:40.166669Z INFO:  new schema: []idk.Field{idk.StringField{NameVal:"asset_tag", DestNameVal:"asset_tag", Mutex:false, Quantum:"", TTL:"", CacheConfig:(*idk.CacheConfig)(nil)}, idk.RecordTimeField{NameVal:"fan_time", DestNameVal:"fan_time", Layout:"2006-01-02", Epoch:time.Date(1, time.January, 1, 0, 0, 0, 0, time.UTC), Unit:""}, idk.StringField{NameVal:"fan_val", DestNameVal:"fan_val", Mutex:false, Quantum:"YMD", TTL:"", CacheConfig:(*idk.CacheConfig)(nil)}}
docker-consumer-csv-consumer-1  | 2022-12-21T22:23:40.191663Z INFO:  translating batch of 8 took: 7.399375ms
docker-consumer-csv-consumer-1  | 2022-12-21T22:23:40.193293Z INFO:  making fragments for batch of 8 took 1.823208ms
docker-consumer-csv-consumer-1  | 2022-12-21T22:23:40.213174Z INFO:  importing fragments took 19.883ms
docker-consumer-csv-consumer-1  | 2022-12-21T22:23:40.247539Z INFO:  1 records processed 0-> (9)
docker-consumer-csv-consumer-1  | 2022-12-21T22:23:40.247732Z INFO:  metrics: import=67.754083ms
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