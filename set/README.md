# Analyzing 5 Billion Games of Set with FeatureBase
FeatureBase is a binary-tree database built on [Roaring Bitmaps](https://roaringbitmap.org/). This makes it suitable for running analytics on massive data sets in real time. If you've never used FeatureBase before, you can [get it running locally in about 5 minutes](https://gist.github.com/kordless/d3aaeedbe0ac68d284c077ddd74c2ae1).

Today, we're going to take a look at using FeatureBase to simulate and analyze a very large number of Set games in real-time.

## Set (the game)
Set is a card game designed by Marsha Falco in 1974 and published by Set Enterprises in 1991. The deck consists of 81 unique cards that vary in four features across three possibilities for each kind of feature: number of shapes (one, two, or three), shape (diamond, squiggle, oval), shading (solid, striped, or open), and color (red, green, or purple).

In a game of Set, the cards are shuffled and then 12 cards are drawn from the top of the deck and placed on the table. Game play then commences by players beginning to identify sets in the initial deal.

In this example, we are going to focus on the initial draw only. We won't be pulling cards and dealing new ones from the remainder of the deck, in other words. We'll simulate one billion draws of twelve cards (from a full deck) and then proceed to do one billion draws of fifteen cards (adding three cards each time) and so on until we have a total of five billion game draws.

## Thinking in Binary
There are 1,080 unique sets possible in the game. Let's think about this for a minute by creating a couple of large binary numbers to look at for visualization. The first number will be 81 digits and represent a single set of of the 1,080 possible sets. We'll also put the different attribute headers at the top of this number to help us figure out what a given binary place represents which card.

We'll use green, purpl, and red for colors. S will respresent squiggles. ♦️ are diamonds and O (ohs) are pills.

```
set_0

<         solid           ><         open            ><         shaded          >
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
< green >< purpl ><  red  >< green >< purpl ><  red  >< green >< purpl ><  red  >
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
<S><♦️><O><S><♦️><O><S><♦️><O><S><♦️><O><S><♦️><O><S><♦️><O><S><♦️><O><S><♦️><O><S><♦️><O>
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
<S><♦️><O><S><♦️><O><S><♦️><O><S><♦️><O><S><♦️><O><S><♦️><O><S><♦️><O><S><♦️><O><S><♦️><O>
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
<S><♦️><O><S><♦️><O><S><♦️><O><S><♦️><O><S><♦️><O><S><♦️><O><S><♦️><O><S><♦️><O><S><♦️><O>
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
