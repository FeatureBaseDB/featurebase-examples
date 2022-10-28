# FeatureBase | Kafka Starter
This example will guide you through getting Kafka set up for ingestion of JSON data into FeatureBase. We'll use a simple schema for this example which generates a user id, name and age:

```
[
    {
        "name": "user_id",
        "path": ["user_id"],
        "type": "string"
    },
    {
        "name": "name",
        "path": ["name"],
        "type": "string"
    },
    {
        "name": "age",
        "path": ["age"],
        "type": "id"
    }
]
```

The process for getting this example going consists of:
1. [Install and start Featurebase](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/kafka-starter#install-and-start-featurebase)
2. [Install and start Kafka](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/kafka-starter#install-and-start-kafka)
3. [Install the Python dependencies](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/kafka-starter#install-dependencies)
4. [Insert sample data using Python](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/kafka-starter#insert-data)

## Clone the Repo
Start a terminal shell and then clone this repo locally (we'll use a `code` directory on macOS in this example):

```
mkdir code
cd code
git clone https://github.com/FeatureBaseDB/featurebase-examples.git
```

Check the directory structure:

```
kord@bob code % ls -lah
drwxr-xr-x    9 kord  staff   288B Oct 27 16:59 featurebase-examples
```

## Install and Start FeatureBase
We'll use a shortened version of the [welcome guide](https://docs.featurebase.com/) for FeatureBase. Refer to the longer version if needed.

In your browser, head over to the [downloads](https://github.com/FeatureBaseDB/FeatureBase/releases) on our [Github repo](https://github.com/FeatureBaseDB/featurebase) and select the build needed for your particular architecture. The ARM versions are for newer Macs or devices like the Raspberry Pi. The AMD versions are for Intel architectures.

Back in the terminal, you'll move the tarball into the current director:

```
mv ~/Downloads/featurebase-*.tar.gz ./
```

Check the directory again:

```
kord@bob code % ls -lah
drwxr-xr-x    9 kord  staff   288B Oct 27 16:59 featurebase-examples
-rw-r--r--@   1 kord  staff    81M Oct 27 11:59 featurebase-v1.1.0-community-darwin-arm64.tar.gz
```

Now use `tar` to uncompress the file:

```
tar xvfz featurebase-*-arm64.tar.gz
```

Let's move the FeatureBase directories into something that's a little easier to type:

```
mv featurebase-*-community-darwin-arm64/ opt
mv idk-*-arm64 idk
```

Here's how all this should look in the `code` directory now:

```
kord@bob code % ls -lah
drwxr-xr-x    9 kord  staff   288B Oct 27 16:59 featurebase-examples
-rw-r--r--@   1 kord  staff    81M Oct 27 11:59 featurebase-v1.1.0-community-darwin-arm64.tar.gz
drwxr-xr-x@   7 kord  staff   224B Oct  1 13:17 idk
drwxr-xr-x@   7 kord  staff   224B Oct  1 13:21 opt

```

### Set File Flags to Run
Before you start the server, you may need to turn off the quarantine flag on the executables so they can run them from the command line (assuming you are using macOS):

```
xattr -d com.apple.quarantine opt/featurebase
xattr -d com.apple.quarantine idk/*
```

**NOTE:** You may need to set the execute flag on the idk/ executables (which you will use here in a minute):

```
chmod 755 idk/*
```

### Start the Server
Start the server by changing into the `opt` directory and running `./featurebase server`:

```
kord@bob ~ % cd ~/Downloads/featurebase/opt
kord@bob fb % ./featurebase server
<snip>
```

## Install and Start Kafka
Apache Kafka is an open-source distributed event streaming platform used by thousands of companies for high-performance data pipelines, streaming analytics, data integration, and mission-critical applications.

We'll be using Kafka to send data to FeatureBase via the Kafka ingestor. We'll be using Python to send data to Kafka.

To install Kafka, head over to Kafka's [download page](https://kafka.apache.org/downloads) in your browser and download one of the binary builds (not the source).


Now use `tar` to uncompress the file:

```
tar xvfz kafka_*.tgz
```




