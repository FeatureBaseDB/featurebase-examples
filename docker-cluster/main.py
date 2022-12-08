import json
import sys
import string
import random
import requests

index_name = "dockercluster"

# cluster port handling
try:
	result = requests.get('http://localhost:10101/status')
	result_object = json.loads(result.text)
	for node in result_object.get('nodes', []):
		if node.get('isPrimary', False) == True:
			cluster_port = node.get('uri', {}).get('port', 10101)
except:
	print("defaulting to port 10101 due to error retreiving cluster primary")
	cluster_port = 10101

# create table and schema
try:
	query = "select count(*) from %s;" % index_name
	result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
	num_records = result.json().get('data')[0][0]
except:
	query = "create table %s (_id id, draw stringset, draw_size id);" % index_name
	result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
	num_records = 0

# cards
card_id = 0
shades = ["●", "#", "○"] # solid, shaded, open
colors = ["P", "R", "G"] # purple, red, green
counts = ["1", "2", "3"] # 1, 2 and 3 shapes
shapes = ["⬯", "~", "◊"] # pills, squiggles, diamonds

cards = []

# generate cards (set the game)
for shade in shades:
	for color in colors:
		for count in counts:
			for shape in shapes:
				card = "%s%s%s%s" % (count, color, shade, shape)
				cards.append(card)

# number of draws and size
print("There are %s existing entries." % num_records)
size = int(input('Enter the draw size (12,15,18,21,24...): '))
num_to_generate = int(input('Enter the number of draws: '))

values = "" # initialize

# loop as many times as needed
for x in range(num_to_generate):
	_draw = "["

	# build the draw stringset
	for y in range(size):
		# this will generate duplicates of cards in the hand....sometimes
		# see the bigdata-set for use of numpy for a proper work around...
		_draw = _draw + "'" + cards[int(random.random()*81)] + "',"
	_draw = _draw.strip(",")
	_draw = _draw + "]"

	# create values	
	values = values + "(%s, %s, %s)," % (x+num_records, _draw, size)

	# batch in thousands
	if x % 1000 == 0:
		query = "INSERT INTO %s VALUES %s" % (index_name, values.strip(","))
		values = "" # reset for next loop

		# insert
		result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
	
	if x % 100000 == 0:
		print("There are %s total records.." % (x+num_records))


# flush last insert
query = "INSERT INTO %s VALUES %s" % (index_name, values.strip(","))
result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
print(result.text)

print("Generated a total of %s draws." % (x+1))
