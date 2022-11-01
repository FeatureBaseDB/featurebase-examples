card_id = 0
shades = ["solid", "shaded", "open"]
colors = ["purple", "red", "green"]
counts = [1,2,3]
shapes = ["squiggle", "pill", "diamond"]

cards = []

# generate cards
for shade in shades:
	for color in colors:
		for count in counts:
			for shape in shapes:
				cards.append({"card_id": card_id, "shade": shade, "color": color, "count": count, "shape": shape})
				card_id = card_id + 1


show = [3, 20, 23, 26, 37, 43, 53, 54, 57, 60, 74, 77]
for s in show:
	for card in cards:
		if card.get("card_id") == s:
			print(card)


