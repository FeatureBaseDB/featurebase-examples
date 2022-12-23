# Examples for FeatureBase
This repository contains guides and example uses of FeatureBase. You may refer to [issues](https://github.com/FeatureBaseDB/featurebase-examples/issues) for a list of inbound examples for this repo.

## Community Edition Examples
- [Simple Docker Deployment](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/docker-simple#readme)
- [Clusterized Docker Deployement](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/docker-cluster#readme)
- [Docker CSV Consumer](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/docker-consumer#readme)
- [FeatureBase + Kafka Consumer in Docker](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/docker-example#readme)
- [FeatureBase + Kafka Manual Setup](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/kafka-starter#readme)

## Cloud Examples
- [Simple Cloud App](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/cloud-simple-webapp#readme)

## Quickstart Featurebase
We'll use a shortened version of the [welcome guide](https://docs.featurebase.com/community/community-setup/community-install-config) for downloading and running FeatureBase on macOS. Refer to the longer version if needed.

Start by heading over to the [downloads](https://github.com/FeatureBaseDB/FeatureBase/releases) on the [Github repo](https://github.com/FeatureBaseDB/featurebase) and select the build needed for your particular architecture.

Open a terminal and move into the directory where you downloaded FeatureBase. Copy and paste these commands to create a new directory and move the tarball into it:

```
mkdir ~/featurebase
mv featurebase-*.tar.gz featurebase
cd featurebase
```

Now use `tar` to uncompress the file:

```
tar xvfz featurebase-*.tar.gz
```

Move the directories:

```
mv featurebase-*/ opt
mv idk-*/ idk
```

### Set File Flags to Run
For macOS, turn off the quarantine flag on the executables:

```
xattr -d com.apple.quarantine opt/featurebase
xattr -d com.apple.quarantine idk/*
```

## Start the Server
Start the server by changing into the `opt` directory and running `./featurebase server`:

```
cd ~/featurebase/opt
./featurebase server
```
## Next Steps
Head over to the [documentation](https://docs.featurebase.com/) for  more information about FeatureBase community edition.
