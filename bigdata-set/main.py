import datetime
import logging
import os, sys
import json
import random

import requests

from flask import Flask
from flask import session, request, redirect
from flask import render_template, make_response
from flask import url_for

from sets import generate_cards, generate_sets, generate_draws, random_string

# app up
app = Flask(__name__)

#@app.route('/')
#def index():
#    return render_template('index.html')

@app.route('/')
def dashboard():
	return render_template('dashboard.html')

@app.route('/sets')
def sets_page():
    return render_template('sets.html')

@app.route('/games')
def games_page():
	return render_template('games.html')

@app.route('/draws')
def draws_page():
	return render_template('draws.html')

@app.route('/api/draw')
def api_draw():
	size = request.args.get('size')
	if not size:
		size = 12
	else:
		size = int(size)

	num_sets = request.args.get('num')
	if not num_sets:
		num_sets = 1000
	else:
		num_sets = int(num_sets)

	draws = generate_draws(size, num_sets)

	values = "" # sql insert string fragment
	for index, draw in enumerate(draws):
		# create values
		name = random_string(size=6)

		
		if len(draw[1]) == 0:
			sets = [9999]
		else:
			sets = draw[1]
		
		# create table bigset (name string, draw idset, sets idset, num_sets int, draw_size int);
		values = values + "('%s', %s, %s, %s, %s)," % (name, draw[0], sets, len(draw[1]), len(draw[0]))

		# batch in thousands
		if index % 10 == 0:
			query = "INSERT INTO bigset VALUES %s" % values.strip(",")
			values = "" # reset for next loop

			# insert
			result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})

	# flush last insert
	query = "INSERT INTO bigset VALUES %s" % values.strip(",")
	result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
	
	return make_response({"result": result.text})

@app.route('/api/draws')
def api_draws():
	# draw size
	size = request.args.get('size')
	if not size:
		size = 12

	num_sets = request.args.get('num_sets')
	if not num_sets:
		num_sets = 2

	draw_id = request.args.get('draw_id')

	data = []
	if not draw_id:
		while True:
			random_card_1 = random.randrange(0,80)

			query = "SELECT TOP(10) * FROM bigset WHERE SETCONTAINS(draw,%s) AND draw_size=%s AND num_sets=%s;" % (random_card_1, size, num_sets)
			result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
			
			results = result.json().get('data')
			if len(results) != 0:
				break

	else:
		query = "SELECT * FROM bigset WHERE _id='%s';" % draw_id
		result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		print(result.text)
		results = result.json().get('data')

	for _result in results:
		card_filenames = []
		for card in _result[1]:
			query = "SELECT * FROM cards WHERE _id=%s" % card
			result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
			f_result = result.json().get('data')[0]
			filename = "%s_%s_%s_%s.PNG" % (f_result[2],f_result[4],f_result[1],f_result[3])
			card_filenames.append(filename)
		
		entry = {
			"id": _result[0],
			"cards": _result[1],
			"sets": _result[2],
			"num_sets": _result[3],
			"draw_size": _result[4],
			"files": card_filenames
		}
		data.append(entry)


	return make_response(data)


@app.route('/api/cards')
def api_cards():
	# draw size
	size = request.args.get('size')
	if not size:
		size = 12

	num_sets = request.args.get('num_sets')
	if not num_sets:
		num_sets = 3

	# data payload
	data = []

	# run a card num range
	for num in range(0,81):
		query = "select count(*) from bigset where setcontains(draw,%s) and draw_size=%s and num_sets=%s;" % (num, size, num_sets)
		result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		print(result.text)
		count = result.json().get('data')[0][0]

		if count != 0:
			data.append({"cards": num, "count": count})
		
	return make_response(data)


@app.route('/api/sets')
def api_sets():
	set_id = request.args.get('set_id')

	if not set_id or set_id == 9999 or set_id == "none":
		set_id = random.randrange(0,1079)

	query = "SELECT * FROM sets WHERE _id=%s;" % set_id
	result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
	results = result.json().get('data')[0]
	
	card_filenames = []
	for card in results[1]:
		query = "SELECT * FROM cards WHERE _id=%s" % card
		result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		f_result = result.json().get('data')[0]
		filename = "%s_%s_%s_%s.PNG" % (f_result[2],f_result[4],f_result[1],f_result[3])
		card_filenames.append(filename)

	data = {
		"set_id": results[0],
		"cards": results[1],
		"files": card_filenames
	}
	return make_response(data)

@app.route('/api/stats')
def api_stats():
	# draw size
	size = request.args.get('size')

	if not size:
		# figure out the different sizes of sets in the db
		query = "SELECT DISTINCT draw_size FROM bigset;"
		result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		results = result.json().get('data')
	else:
		results = []
		results.append([int(size)])

	stats = []
	for draw_size in results:
		# counts
		query = "SELECT COUNT(*) FROM bigset WHERE draw_size=%s;" % draw_size[0]
		result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		count = result.json().get('data')[0][0]

		# max sets in draw
		query = "SELECT MAX(num_sets) FROM bigset WHERE draw_size=%s;" % draw_size[0]
		result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		max_sets = result.json().get('data')[0][0]

		# max sets in draw
		query = "SELECT MIN(num_sets) FROM bigset WHERE draw_size=%s;" % draw_size[0]
		result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		min_sets = result.json().get('data')[0][0]

		# totals sets in all draws
		query = "SELECT SUM(num_sets) FROM bigset WHERE draw_size=%s;" % draw_size[0]
		result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		total_sets = result.json().get('data')[0][0]

		# no sets in all draws
		query = "SELECT COUNT(*) FROM bigset WHERE draw_size=%s AND num_sets=0;" % draw_size[0]
		result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		no_sets = result.json().get('data')[0][0]

		stats.append({"draw_size": draw_size[0], "count": count, "max_sets": max_sets, "min_sets": min_sets, "total_sets": total_sets, "no_sets": no_sets})

	return make_response(stats)

@app.route('/api/chart')
def api_chart():
	# draw size
	size = request.args.get('size')

	if not size:
		# max sets in draw
		query = "SELECT MAX(num_sets) FROM bigset;"
		result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		max_sets = result.json().get('data')[0][0]

		# draw sizes
		query = "SELECT DISTINCT draw_size FROM bigset;"
		result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		draw_sizes = result.json().get('data')
	else:
		# max sets in draw
		query = "SELECT MAX(num_sets) FROM bigset WHERE draw_size=%s;" % size
		result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		max_sets = result.json().get('data')[0][0]

		# set draw sizes array to size
		draw_sizes = [[size]]

	# data payload
	data = []

	# run a count range
	for draw_size in draw_sizes:
		for num_sets in range(0,max_sets+1):
			query = "select count(*) from bigset where num_sets=%s and draw_size=%s;" % (num_sets, draw_size[0])
			result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
			count = result.json().get('data')[0][0]

			if count != 0:
				data.append({"num_sets": num_sets, "draw_size": draw_size[0], "count": count})
			
	return make_response(json.dumps(data))


if __name__ == '__main__':
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

	# create cards
	try:
		query = "select count(*) from cards;"
		result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		num_records = result.json().get('data')[0][0]
		print("%s cards found" % num_records)
		if num_records == 0:
			raise("no cards found")
	except:
		print("generating cards")
		cards = generate_cards()

		query = "create table cards (_id id, shade string, color string, count string, shape string);"
		result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})

		for card in cards:
			values = "(%s, '%s', '%s', '%s', '%s')" % (card.get('card_id'), card.get('shade'), card.get('color'), card.get('count'), card.get('shape'))

			# insert
			query = "INSERT INTO cards VALUES %s" % values.strip(",")
			result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})

	# create sets
	try:
		query = "select count(*) from sets;"
		result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		num_records = result.json().get('data')[0][0]
		print("%s sets found" % num_records)
		if num_records == 0:
			raise("no sets found")
	except:
		print("generating valid sets")
		sets = generate_sets()

		query = "create table sets (_id id, cards idset);"
		result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})

		for index, _set in enumerate(sets):
			values = "(%s, %s)" % (index, _set)
			
			# insert
			query = "INSERT INTO sets VALUES %s" % values.strip(",")
			result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})

	# create bigset (draws of cards with sets detected)
	try:
		query = "select count(*) from bigset;"
		result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		num_records = result.json().get('data')[0][0]
		print("%s draws found" % num_records)

		if num_records == 0:
			raise("no draws found")
	except Exception as ex:
		print("generating draws")
		query = "create table bigset (_id string, draw idset, sets idset, num_sets int, draw_size int);"
		url = 'http://localhost:%s/sql' % cluster_port
		result = requests.post(url, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})

		# generate a few
		draws = generate_draws(num_to_generate=100)

		values = ""
		for draw in draws:
			name = random_string(size=6)

			if len(draw[1]) == 0:
				sets = [9999]
			else:
				sets = draw[1]

			# quote the string and build insert
			values = values + "('%s', %s, %s, %s, %s)," % (name, draw[0], sets, len(draw[1]), len(draw[0]))

		query = "INSERT INTO bigset VALUES %s" % values.strip(",")
		
		# insert
		result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})

	# This is used when running locally.
	# app.run(host='127.0.0.1', port=8000, debug=True)
	app.run(host='localhost', port=8000, debug=True)
	dev = True
