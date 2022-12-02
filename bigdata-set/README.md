# Analyzing Millions of Draws of Set the Game with FeatureBase
[FeatureBase](https://featurebase.com/) is a binary-tree database built on [Roaring Bitmaps](https://roaringbitmap.org/). This makes it suitable for running analytics on massive data sets in real time.

Today, we're going to take a look at using FeatureBase to simulate and analyze a very large number of draw of [Set the Game](https://en.wikipedia.org/wiki/Set_(card_game)) in real-time.

## Set (the game)
Set is a card game designed by Marsha Falco in 1974 and published by Set Enterprises in 1991. The deck consists of 81 unique cards that vary in four features across three possibilities for each kind of feature: number of shapes (one, two, or three), shape (diamond, squiggle, oval), shading (solid, striped, or open), and color (red, green, or purple).

In a game of Set, the cards are shuffled and then 12 cards are drawn from the top of the deck and placed on the table. Game play then commences by players beginning to identify sets in the initial deal. If a set is not found in the initial draw, 3 cards are added to the draw until a set is found.

Here's an example draw of 12 cards that has 12 different sets in it:

![sets](https://github.com/featurebaseDB/featurebase-examples/main/bigdata-set/static/setdraw.png)

In this example, we are going to focus on the initial draws only. We won't be pulling cards and dealing new ones from the remainder of the deck. We'll simulate millions of draws from deals of 12, 15 and 18 cards each.

## Run FeatureBase



