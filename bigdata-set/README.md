# Analyzing Millions of Draws of Set the Game with FeatureBase
[FeatureBase](https://featurebase.com/) is a binary-tree database built on [Roaring Bitmaps](https://roaringbitmap.org/). This makes it suitable for running analytics on massive data sets in real time.

Today, we're going to take a look at using FeatureBase to simulate and analyze a very large number of draws of [Set the Game](https://en.wikipedia.org/wiki/Set_(card_game)) in real-time.

You may be interested in discussions about the probabilities for the game:

[Investigations into the Card Game SET](https://www.setgame.com/sites/default/files/teacherscorner/SETPROOF.pdf)
[The Card Game SET](http://homepages.warwick.ac.uk/staff/D.Maclagan/papers/set.pdf)
[The Odds of Finding a SET in The Card Game SET®](http://norvig.com/SET.html)

## Set (the game)
Set is a card game designed by Marsha Falco in 1974 and published by Set Enterprises in 1991. The deck consists of 81 unique cards which vary in four different features: number of shapes (one, two, or three), shape (diamond, squiggle, or oval), shading (solid, striped, or open), and color (red, green, or purple). 

In a game of Set, the cards are shuffled and then 12 cards are drawn from the top of the deck and placed on the table. Players must then try to identify sets within this initial draw. If no sets are found, 3 more cards are added until a set is identified. 

As an example, a draw of 12 cards could contain 12 different sets:

![sets](https://raw.githubusercontent.com/FeatureBaseDB/featurebase-examples/main/bigdata-set/static/setdraw.png)

Like this example, we are going to focus on intial draws only. We won't be pulling sets from the board or dealing new ones from the remainder of the deck. We'll simulate millions of draws from deals of 12, 15 and 18 cards each.

## Run FeatureBase
This example requires FeatureBase is running on your computer. To get FeatureBase running quickly, ensure you have Docker installed and then begin by cloning this repository locally:

```
git clone https://github.com/FeatureBaseDB/featurebase-examples.git
cd featurebase-examples/docker-simple
```

Start the FeatureBase container:

```
docker-compose up -d
```

A more detailed guide for starting FeatureBase is available [here](https://github.com/FeatureBaseDB/featurebase-examples/tree/main/docker-simple#readme).



