from numpy.random import default_rng

rng = default_rng()



def all_same_or_all_diff (attr1, attr2, attr3):
	if attr1 == attr2 and attr2 == attr3:
		return True
	elif (attr1 != attr2) and (attr2 != attr3) and (attr3 != attr1):
		return True
	else:
		return False

card_id = 0
shades = ["solid", "shaded", "open"]
colors = ["purple", "red", "green"]
counts = [1,2,3]
shapes = ["squiggle", "pill", "diamond"]

cards = []

for shade in shades:
	for color in colors:
		for count in counts:
			for shape in shapes:
				cards.append({"card_id": card_id, "shade": shade, "color": color, "count": count, "shape": shape})
				card_id = card_id + 1


for x in range(2000):
	draw = sorted(rng.choice(81, size=12, replace=False))
	sets = []
	set_count = 0
	for draw_card_1 in draw:
		for draw_card_2 in draw:
			if draw_card_2 != draw_card_1:
				for draw_card_3 in draw:
					if draw_card_3 != draw_card_2 and draw_card_3 != draw_card_1:
						if all_same_or_all_diff(cards[draw_card_1].get("shade"), cards[draw_card_2].get("shade"), cards[draw_card_3].get("shade")):
							if all_same_or_all_diff(cards[draw_card_1].get("color"), cards[draw_card_2].get("color"), cards[draw_card_3].get("color")):
								if all_same_or_all_diff(cards[draw_card_1].get("count"), cards[draw_card_2].get("count"), cards[draw_card_3].get("count")):
									if all_same_or_all_diff(cards[draw_card_1].get("shape"), cards[draw_card_2].get("shape"), cards[draw_card_3].get("shape")):
										hand = sorted([draw_card_1, draw_card_2, draw_card_3])

										if hand not in sets:
											sets.append(hand)
											set_count = set_count + 1
	print(draw)
	for _set in sets:
		print("==================")
		for card in _set:
			print(cards[card]),

