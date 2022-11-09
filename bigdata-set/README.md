# Analyzing 5 Billion Games of Set with FeatureBase
FeatureBase is a binary-tree database built on [Roaring Bitmaps](https://roaringbitmap.org/). This makes it suitable for running analytics on massive data sets in real time. If you've never used FeatureBase before, you can [get it running locally in about 5 minutes](https://gist.github.com/kordless/d3aaeedbe0ac68d284c077ddd74c2ae1).

Today, we're going to take a look at using FeatureBase to simulate and analyze a very large number of Set games in real-time.

## Set (the game)
Set is a card game designed by Marsha Falco in 1974 and published by Set Enterprises in 1991. The deck consists of 81 unique cards that vary in four features across three possibilities for each kind of feature: number of shapes (one, two, or three), shape (diamond, squiggle, oval), shading (solid, striped, or open), and color (red, green, or purple).

In a game of Set, the cards are shuffled and then 12 cards are drawn from the top of the deck and placed on the table. Game play then commences by players beginning to identify sets in the initial deal.

In this example, we are going to focus on the initial draw only. We won't be pulling cards and dealing new ones from the remainder of the deck, in other words. We'll simulate one billion draws of twelve cards (from a full deck) and then proceed to do one billion draws of fifteen cards (adding three cards each time) and so on until we have a total of five billion game draws.

# FeatureBase | Kafka Starter
This example will guide you through getting Kafka set up for ingestion of JSON data into FeatureBase using Python. We'll use a simple schema for this example which uses `user_id`, `name` and `age`:

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
1. [Install and start Kafka](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/kafka-starter#install-and-start-kafka)
1. [Start the Kafka consumer](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/kafka-starter#start-the-ingestor)
1. [Install the Python dependencies](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/kafka-starter#install-the-requirements)
1. [Insert set data using Python](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/kafka-starter#run-the-script)
1. [Query and visualize data]()

## Clone the Repo
Start a terminal shell and then clone this repo locally (we'll use a `binary` directory on macOS in this example):

```
mkdir binary
cd binary
git clone https://github.com/FeatureBaseDB/featurebase-examples.git
```

Check the directory structure:

```
kord@bob binary % ls -lah
drwxr-xr-x    9 kord  staff   288B Oct 27 16:59 featurebase-examples
```

## Install and Start FeatureBase
We'll use a shortened version of the [welcome guide](https://docs.featurebase.com/) for running FeatureBase.

In your browser, head over to the [downloads](https://github.com/FeatureBaseDB/FeatureBase/releases) on the [Github repo](https://github.com/FeatureBaseDB/featurebase) and select the builds needed for your particular architecture. The ARM versions are for newer Macs or devices like the Raspberry Pi. The AMD versions are for Intel architectures.

Back in the terminal, you'll move the tarballs into the current directory:

```
mv ~/Downloads/featurebase-*.tar.gz ./
```

Check the directory again:

```
kord@bob binary % ls
featurebase-examples
featurebase-v1.2.0-community-darwin-arm64.tar.gz
```

Now use `tar` to un-compress the files:

```
tar xvfz featurebase-*.tar.gz
```

Let's move the directories into something that's a little easier to type:

```
mv featurebase-*-arm64/ opt
mv idk-*-arm64 idk
```

Now remove the offending tarballs (optional AND BE CAREFUL WITH THIS):

```
rm *.gz*
```

Here's how all this should look in the `binary` directory now:

```
kord@bob binary % ls -lah
drwxr-xr-x    9 kord  staff   288B Oct 27 16:59 featurebase-examples
drwxr-xr-x@   7 kord  staff   224B Oct 28 13:17 idk
drwxr-xr-x@   7 kord  staff   224B Oct 28 13:21 opt

```

### Set File Flags to Run
Before you start the server, you may need to turn off the quarantine flag on the executables so they can run them from the command line (assuming you are using macOS):

```
xattr -d com.apple.quarantine opt/featurebase
xattr -d com.apple.quarantine idk/*
```

### Start the Server
Start the server by changing into the `opt` directory and running `./featurebase server`:

```
kord@bob ~ % cd opt
kord@bob opt % ./featurebase server
<snip>
```

## Install and Start Kafka
Apache Kafka is an open-source distributed event streaming platform used by thousands of companies for high-performance data pipelines, streaming analytics, data integration, and mission-critical applications.

We'll be using Kafka to send data to FeatureBase via the Kafka consumer.

To install Kafka, head over to Kafka's [download page](https://kafka.apache.org/downloads) in your browser and download one of the binary builds. Which one doesn't matter, just don't download the source tarball.

In a new terminal, move the tarball into `binary` and use `tar` to un-compress the file:

```
cd ~/binary
mv ~/Downloads/kafka_*.tgz ./
tar xvfz kafka_*.tgz
```

Now remove the tarball:

```
rm kafka_*.tgz
```

Here's the directory structure you should have now:

```
kord@bob binary % ls
featurebase-examples    idk                     kafka_2.13-3.3.1        opt
```

### Start Kafka
Now we have all the components in place, let's move into the Kafka directory and start the Zookeeper server:

```
cd kafka_*
./bin/zookeeper-server-start.sh config/zookeeper.properties
```

Open a new terminal window, move back into the Kafka directory and start Kafka:

```
cd ~/binary/kafka_*
./bin/kafka-server-start.sh config/server.properties
```

### Create a Kafka Topic
Kafka uses the idea of `topics` to route data. Open a new terminal window, move into the Kafka directory and run the following to create a topic called `allyourbase`:

```
cd ~/binary/kafka_*
./bin/kafka-topics.sh --create --topic allyourbase --bootstrap-server localhost:9092
```

**OUTPUT:**
```
kord@bob kafka_2.13-3.3.1 % ./bin/kafka-topics.sh --create --topic allyourbase --bootstrap-server localhost:9092
Created topic allyourbase.
```

## Start the Consumer
FeatureBase uses an consumer process to fetch data from Kafka for ingestion into the FeatureBase index. To start the consumer process, let's move back up a directory and into the examples repo directory:

```
kord@bob kafka_2.13-3.3.1 % cd ../featurebase-examples/kafka-starter/
kord@bob kafka-starter % ls
README.md               requirements.txt        schema.json             utils
main.py                 sample.json             start-consumer.sh
```

To start the consumer, run the `start-consumer.sh` script. If you want to use a topic name other than `allyourbase`, edit the file and change it to your preferred topic name.

```
kord@bob kafka-starter % bash start-consumer.sh
Molecula Consumer v3.21.0, build time 2022-09-29T17:54:10+0000
2022-10-29T14:54:16.043784Z INFO:  Serving Prometheus metrics with namespace "ingester_kafka_static" at localhost:9093/metrics
2022-10-29T14:54:16.048390Z INFO:  sourced 0 records in 4.083µs
<snip>
```

**NOTE:**
If you want to change the schema to match your own data layout, you will need to edit the `schema.json` file and restart the consumer process.

## Review Processes
At this point in the guide, you will have four separate tabs in your terminal running processes. Here are the processes that should be running:

1. The FeatureBase process.
1. The Zookeeper process.
1. The Kafka process.
1. The FeatureBase Kafka consumer.

## Thinking in Binary
There are 1,080 unique sets possible in the game. Let's think about this for a minute by creating a couple of large binary numbers to look at for visualization. The first number will be 81 digits and represent a single set of of the 1,080 possible sets. We'll also put the different attribute headers at the top of this number to help us figure out what a given binary place represents which card.

We'll use green, purpl, and red for colors. S will respresent squiggles. ♦️ are diamonds and O (ohs) are pills.

```
set_0

<         solid           ><         open            ><         shaded          >
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
< green >< purpl ><  red  >< green >< purpl ><  red  >< green >< purpl ><  red  >
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
<S><♦><O><S><♦><O><S><♦><O><S><♦><O><S><♦><O><S><♦><O><S><♦><O><S><♦><O><S><♦><O>
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
123123123123123123123123123123123123123123123123123123123123123123123123123123123
---------------------------------------------------------------------------------
100000000100000000100000000000000000000000000000000000000000000000000000000000000
```

In this representation, we are saying we have a solid green squggle of count one, a solid purple squiggle of count one and a solid red squiggle of count one. This is a set because all the attributes are either different (colors in this example) or all the same (shading, count and shape).

Now let's do one where the three cards have different shading, color, count and shape:

```
set_1

<         solid           ><         open            ><         shaded          >
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
< green >< purpl ><  red  >< green >< purpl ><  red  >< green >< purpl ><  red  >
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
<S><♦><O><S><♦><O><S><♦><O><S><♦><O><S><♦><O><S><♦><O><S><♦><O><S><♦><O><S><♦><O>
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
123123123123123123123123123123123123123123123123123123123123123123123123123123123
---------------------------------------------------------------------------------
001000000000000000000000000000000000000000000000000010000000000000100000000000000
```


Now we'll do a sample draw of 15 cards.

```
draw_0

<         solid           ><         open            ><         shaded          >
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
< green >< purpl ><  red  >< green >< purpl ><  red  >< green >< purpl ><  red  >
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
<S><♦><O><S><♦><O><S><♦><O><S><♦><O><S><♦><O><S><♦><O><S><♦><O><S><♦><O><S><♦><O>
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
123123123123123123123123123123123123123123123123123123123123123123123123123123123
---------------------------------------------------------------------------------
100011000100000000100000010100000000000010000010000000101100000100000010010000000
---------------------------------------------------------------------------------
```

Here's what that draw looks like, in a real game:

![open](https://gist.github.com/kordless/9c5b1f0fa0a57bb5c9101a99f3cc5e70/raw/3ef3e2bec09beae895704a162ddc4dc20c9c348b/set.png)

Now we AND the two numbers:

```
---------------------------------------------------------------------------------
100000000100000000100000000000000000000000000000000000000000000000000000000000000
100011000100000000100000010100000000000010000010000000101100000100000010010000000
---------------------------------------------------------------------------------
100000000100000000100000000000000000000000000000000000000000000000000000000000000
```

Given that result is equivalent to the the set we mention above, we have a match. There may be other sets present on the board, but we're going to switch to using decimal numbers to respresent the different cards.

## Modeling
As there are 81 total cards, we're going to use 0 through 80 to represent those cards. So, a sample draw of those same 15 cards above now becomes:

```
[0,4,5,9,18,25,27,40,46,54,56,57,63,70,73]
```

As for our sample set we chose, that becomes:

```
[0,9,18]
```

We need a list of valid sets.
