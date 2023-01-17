# Analyzing Millions of Draws of Set the Game with FeatureBase 
Today, we're going to take a look at using [FeatureBase](https://featurebase.com/) to analyze a very large number of draws of [Set the Game](https://en.wikipedia.org/wiki/Set_(card_game)) in real-time.

## Set (the game)
Set is a card game designed by Marsha Falco in 1974 and published by Set Enterprises in 1991. The deck consists of 81 unique cards which vary in four different features: number of shapes (one, two, or three), shape (diamond, squiggle, or oval), shading (solid, dashed, or open), and color (red, green, or purple). 

You may be interested in this paper about the probabilities for the game:

- [Investigations into the Card Game SET](https://www.setgame.com/sites/default/files/teacherscorner/SETPROOF.pdf)

In a game of Set, the cards are shuffled and then 12 cards are drawn from the top of the deck and placed on the table. Players must then try to identify sets within this initial draw. If no sets are found, 3 more cards are added until a set is identified. 

As an example, a draw of 12 cards could contain 13 different sets:

![sets](https://raw.githubusercontent.com/FeatureBaseDB/featurebase-examples/main/bigdata-set/static/setdraw2.png)


Here is the probability table for different draw amounts. Notice that a 12 card draw may have up to 14 sets in it, although it is very unlikely to find one.

![sets](https://raw.githubusercontent.com/FeatureBaseDB/featurebase-examples/main/bigdata-set/static/prob_table.png)

## The Application
This application will generate a variety of 12, 15, 18, 21, and 24 card draws of the game. Generation happens when you go to the dashboard page OR the games page for a draw size, and both those pages will update as new draws are generated.

You may be interested in [the code](https://github.com/FeatureBaseDB/featurebase-examples/blob/main/bigdata-set/main.py) for bulk ingestion and querying via FeatureBase's SQL implementation. 

The application doesn't allow pulling sets from the board or dealing new ones from the remainder of the deck, but we can simulate millions of draws and report on them very quickly using FeatureBase's functions.

Here's what the dashboard of the application looks like:

![dash](https://raw.githubusercontent.com/FeatureBaseDB/featurebase-examples/main/bigdata-set/static/dash.png)


## Run FeatureBase
This example requires FeatureBase running on your computer. To get FeatureBase running quickly, ensure you have git and Docker installed and then begin by cloning this repository locally:

```
git clone https://github.com/FeatureBaseDB/featurebase-examples.git
cd featurebase-examples/docker-simple
```

Start the FeatureBase container:

```
docker-compose up -d
```

A more detailed guide for starting FeatureBase is available [here](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/docker-simple#readme).

## Install Requirements
To run this applicationj, you will need to install a few Python libraries. To install these automatically, run the following:

```
pip3 install -r requirements.txt
```

## Run the Dashboard
Start the application by running the following:

```
python3 main.py
```

*OUTPUT*:
```
81 cards found
1080 sets found
14009373 draws found
 * Debugger is active!
 * Debugger PIN: 178-522-378
 * Running on http://localhost:8000
Press CTRL+C to quit
```

To view the application, open a browser and enter:

```
http://localhost:8000
```

## Screenshots
Showing a few million 12 card draws, up to draws containing 13 sets:

![screen_2](https://raw.githubusercontent.com/FeatureBaseDB/featurebase-examples/main/bigdata-set/static/screen_2.png)


Showing the cards in draws containing 12 cards and 13 sets:

![screen_3](https://raw.githubusercontent.com/FeatureBaseDB/featurebase-examples/main/bigdata-set/static/screen_3.png)


Showing a particular set, contained in the draw:

![screen_4](https://raw.githubusercontent.com/FeatureBaseDB/featurebase-examples/main/bigdata-set/static/screen_4.png)

## Community
If you enjoyed this example, head over to our community and say hello!

https://discord.com/invite/featurefirstai
