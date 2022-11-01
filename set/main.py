import json
import sys
import string
import random

from coolname import generate_slug
from bson import json_util

# import kafka and define producer
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# random strings for IDs
def random_string(size=6, chars=string.ascii_letters + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

# schema
"""
[
    {
        "name": "card_id",
        "path": ["card_id"],
        "type": "int"
    },
    {
        "name": "draw",
        "path": ["draw"],
        "type": "ids"
    }
]
"""

from numpy.random import default_rng
import numpy as np

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

# generate cards
for shade in shades:
	for color in colors:
		for count in counts:
			for shape in shapes:
				cards.append({"card_id": card_id, "shade": shade, "color": color, "count": count, "shape": shape})
				card_id = card_id + 1

# generate valid sets
valid_sets = []
for card_1 in cards:
	for card_2 in cards:
		if card_2 != card_1:
			for card_3 in cards:
				if card_3 != card_2 and card_3 != card_1:
					if all_same_or_all_diff(card_1.get("shade"), card_2.get("shade"), card_3.get("shade")):
						if all_same_or_all_diff(card_1.get("color"), card_2.get("color"), card_3.get("color")):
							if all_same_or_all_diff(card_1.get("count"), card_2.get("count"), card_3.get("count")):
									if all_same_or_all_diff(card_1.get("shape"), card_2.get("shape"), card_3.get("shape")):
											hand = sorted([card_1.get("card_id"), card_2.get("card_id"), card_3.get("card_id")])
											if hand not in valid_sets:
												valid_sets.append(hand)

# create numpy array of the sets
np_sets = np.array(valid_sets)

# function to look for the index of the sets we find
def find_index(arr, x):
    return np.where((arr == x).all(axis=1))[0]

# number of draws
num_to_generate = 1000000

# draws									
for x in range(num_to_generate):
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
	
	for _set in sets:
		set_array = np.array(_set, dtype='uint8')
		data = {"draw": x, "set": int(find_index(np_sets, set_array)[0]), "num_sets": len(sets)}
		producer.send('allyourbase', json.dumps(data, default=json_util.default).encode('utf-8'))

	for card in draw:
		data = {"card_id": int(card), "draw": int(x)}

		producer.send('allyourbase', json.dumps(data, default=json_util.default).encode('utf-8'))

# flush the producer
producer.flush()