# FeatureBase with a Simple Docker Deployment
This guide covers starting FeatureBase using a simple Docker compose file and ingesting a moderate amount of data using a Python script. A container is started running a standalone instance of FeatureBase and exposes port `10101` for querying and ingestion.

Ingestion is done using Python through the `main.py` file.

If you want to ingest data with a CSV consumer, see the [docker-consumer](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/docker-consumer) example in this repo.

**Note**:
You can run a consumer on the host machine directly to insert into this example's Dockerized FeatureBase, but you will need to map the `featurebase` hostname in the local host's `/etc/hosts` file first:


```
featurebase    127.0.0.1
```

If you would like to start an instance of FeatureBase configured for Kafaka ingestion, see the [docker-example](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/docker-example) in this repo.

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

If you want to use the default `bridge` network, delete the network section:

```
networks:
  default:
    name: fbnet
    external: true
```

## Start the Services
Start the services using `docker-compose`:

```
docker compose up
```

**NOTE**: If you have issues with `docker compose`, try disabling v2 by going into *settings..general* in Docker Desktop.

You should now have a container running:

![screenshot](container.png)

## Run the Insert Script
The script inserts "draws" of 81 different cards from *Set the Game*. The cards are represented with strings. For example, `3G#~` is shorthand for 3 green shaded squiggles. 

Before you run the script, ensure you have the requirements installed:

```
pip3 install -r requirements.txt
```

Now run the script to insert data:

```
% python3 main.py
```

**OUTPUT**:

```
% python3 main.py
There are 1201000 existing records.
Enter the draw size (12,15,18,21,24...): 12
Enter the number of draws: 1000000
There are 1201000 total records..
There are 1301000 total records..
<a few seconds later>
There are 2101000 total records..
Generated a total of 1000000 draws.
```

## Use the UI to Query with SQL
To check this worked, in your browser head over to `http://0.0.0.0:10101` and run the following query:

```
select count(*) from simpledocker where draw='3G#~';
```

![ui](counts.png)

Try other queries to run:

```
select * from simpledocker where draw='3G#~' and draw='2G#~' and draw='1G#~';
```

or

```
select * from simpledocker where draw='3G#~' order by draw limit 10;
```

## Tear It Down
To remove the deployment run the following:

```
docker-compose down 
```

In the next guide we'll explore adding a few million draws of `Set the Game` into FeatureBase and reporting on the draws using graphs.

If you liked this guide, be sure to [join the Discord](https://discord.com/invite/bSBYjDbUUb) and give us a shout!


