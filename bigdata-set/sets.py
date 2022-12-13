import json
import sys
import string
import random
import requests

from coolname import generate_slug

from numpy.random import default_rng
import numpy as np

# random strings for IDs
def random_string(size=6, chars=string.ascii_letters + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


# function to look for the index of the sets we find in a draw
def find_index(arr, x):
	return np.where((arr == x).all(axis=1))[0]


def generate(size=12, num_to_generate=10000, num_records=0, cluster_port=10101):
	# random range
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

	# first loop through all cards in deck
	for card_1 in cards:
		# second loop through all cards in deck
		for card_2 in cards:
			# simple check to make sure cards aren't the same
			if card_2 != card_1:
				# third loop through all cards in deck
				for card_3 in cards:
					# another check cards aren't the same
					if card_3 != card_2 and card_3 != card_1:

						# check the shade
						if all_same_or_all_diff(card_1.get("shade"), card_2.get("shade"), card_3.get("shade")):
							# check the color
							if all_same_or_all_diff(card_1.get("color"), card_2.get("color"), card_3.get("color")):
								# check the count
								if all_same_or_all_diff(card_1.get("count"), card_2.get("count"), card_3.get("count")):
									# check the shape
									if all_same_or_all_diff(card_1.get("shape"), card_2.get("shape"), card_3.get("shape")):

										# a draw of three cards is now in "hand", so we sort it
										hand = sorted([card_1.get("card_id"), card_2.get("card_id"), card_3.get("card_id")])

										# check if the three cards are in the list of valid sets
										if hand not in valid_sets:
											# add them to the list of valid sets
											valid_sets.append(hand)


	# create numpy array of all the possible sets
	np_sets = np.array(valid_sets)

	# create a list of draws
	data_frame = []
	values = ""							
	for x in range(num_to_generate):
		draw_id = random_string(size=8)
		_draw = sorted(rng.choice(81, size=size, replace=False))

		_draw_sets = []

		set_count = 0
		for draw_card_1 in _draw:
			for draw_card_2 in _draw:
				if draw_card_2 != draw_card_1:
					for draw_card_3 in _draw:
						if draw_card_3 != draw_card_2 and draw_card_3 != draw_card_1:
							if all_same_or_all_diff(cards[draw_card_1].get("shade"), cards[draw_card_2].get("shade"), cards[draw_card_3].get("shade")):
								if all_same_or_all_diff(cards[draw_card_1].get("color"), cards[draw_card_2].get("color"), cards[draw_card_3].get("color")):
									if all_same_or_all_diff(cards[draw_card_1].get("count"), cards[draw_card_2].get("count"), cards[draw_card_3].get("count")):
										if all_same_or_all_diff(cards[draw_card_1].get("shape"), cards[draw_card_2].get("shape"), cards[draw_card_3].get("shape")):
											grab = sorted([draw_card_1, draw_card_2, draw_card_3])

											# add the set found in the draw to _draw_sets
											if grab not in _draw_sets:
												_draw_sets.append(grab)
												set_count = set_count + 1

		# create a list of IDs for the valid sets in the draw
		_set_ids = []
		for _set in _draw_sets:
			set_array = np.array(_set, dtype='uint8')
			# look up the set ID
			_set_ids.append(int(find_index(np_sets, set_array)[0]))

		# convert the drawn card IDS to ints (from numpy int64s)
		draw = []
		for _card_id in _draw:
			draw.append(int(_card_id))


		# test sets found
		if len(_set_ids) == 0:
			_set_ids.append(9999)
			num_sets = 0
		else:
			num_sets = len(_set_ids)

		# create values	
		values = values + "(%s, %s, %s, %s, %s)," % (x+num_records, draw, _set_ids, num_sets, size)

		# batch in thousands
		if x % 1000 == 0:
			query = "INSERT INTO bigset VALUES %s" % values.strip(",")
			values = "" # reset for next loop

			# insert
			result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		
		if x % 100000 == 0:
			print("There are %s total entries..." % (x+num_records))

	query = "INSERT INTO bigset VALUES %s" % values.strip(",")

	result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
	print(result.text)
	print("Generated a total of %s draws." % (x+1))