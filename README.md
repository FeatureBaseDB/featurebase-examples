# Examples for FeatureBase
This repositoriy contains guides and example uses of FeatureBase. You may refer to [issues](https://github.com/FeatureBaseDB/featurebase-examples/issues) for a list of inbound examples for this repo.

## Community Edition Examples
- [FeatureBase + Kafka in Docker](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/docker-example#readme)
- [FeatureBase + Kafka Manual Setup](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/kafka-starter#readme)

## Cloud Examples
- [Simple Cloud App](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/simple-cloud-webapp#readme)

## Install and Start Featurebase
We'll use a shortened version of the [welcome guide](https://docs.featurebase.com/community/community-setup/community-install-config) for FeatureBase. Refer to the longer version if needed.

Start by heading over to the [downloads](https://github.com/FeatureBaseDB/FeatureBase/releases) on the [Github repo](https://github.com/FeatureBaseDB/featurebase) and select the build needed for your particular architecture.

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

Move the directories:

```
mv featurebase-*-community-darwin-arm64/ opt
mv idk-*-arm64 idk
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
cd ~/Downloads/featurebase/opt
./featurebase server
```

