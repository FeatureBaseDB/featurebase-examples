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

## Install and Start FeatureBase
We'll use a shortened version of the [welcome guide](https://docs.featurebase.com/) for FeatureBase. Refer to the longer version if needed.

Start by heading over to the [downloads](https://github.com/FeatureBaseDB/FeatureBase/releases) on the [Github repo](https://github.com/FeatureBaseDB/featurebase) and select the build needed for your particular architecture. The ARM version are for newer Macs or devices like the Raspberry Pi. The AMD versions are for Intel architectures.

Open a terminal and move into the directory where you downloaded FeatureBase. Copy and paste these commands to create a new directory and move the tarball into it:

```
mkdir featurebase
mv featurebase-*.tar.gz featurebase
cd featurebase
```

Now use `tar` to uncompress the file:

```
tar xvfz featurebase-*-arm64.tar.gz
```

Let's move the directories into something that's a little easier to type:

```
mv featurebase-*-community-darwin-arm64/ opt
mv idk-*-arm64 idk
```

### Set File Flags to Run
Before you start the server, you may need to turn off the quarantine flag on the executables so they can run them from the command line (assuming you are using macOS):

```
xattr -d com.apple.quarantine opt/featurebase
xattr -d com.apple.quarantine idk/*
```

**NOTE:** You may need to set the execute flag on the idk/ executables:

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
