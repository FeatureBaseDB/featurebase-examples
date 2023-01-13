import datetime
import logging
import os, sys
import json

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

@app.route('/sets')
def sets_page():
    return render_template('setss.html')

@app.route('/draws')
def draws_page():
	return render_template('draws.html')

@app.route('/cards')
def cards_page():
	return render_template('cards.html')

@app.route('/')
def dashboard():
	return render_template('dashboard.html')

@app.route('/api/draw')
def api_draw():
	print("generating draws")
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
		if index % 1000 == 1000:
			query = "INSERT INTO bigset VALUES %s" % values.strip(",")
			values = "" # reset for next loop

			# insert
			result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})

	# flush last insert
	query = "INSERT INTO bigset VALUES %s" % values.strip(",")
	result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
	
	return make_response({"result": result.text})

@app.route('/api/cards')
def api_cards():
	# draw size
	size = request.args.get('size')
	if not size:
		size = 12

	num_sets = request.args.get('num_sets')
	if not num_sets:
		num_sets = 0

	# data payload
	data = []

	# run a card num range
	for num in range(0,81):
		query = "select count(*) from bigset where setcontains(draw,%s) and draw_size=%s and num_sets=%s;" % (num, size, num_sets)
		result = requests.post('http://0.0.0.0:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		print(result.text)
		count = result.json().get('data')[0][0]

		if count != 0:
			data.append({"cards": num, "count": count})
		
	return make_response(data)


@app.route('/api/stats2')
def api_stats2():
	# data payload
	data = []

	# run a count range
	for draw_size in [12, 15, 18, 21]:
		query = "select count(*) from bigset where num_sets = %s and draw_size = %s;" % (num, size)

		result = requests.post('http://0.0.0.0:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})

		count = result.json().get('data')[0][0]

		if count != 0:
			data.append({"num_sets": num, "count": count})
			
	return make_response(data)

@app.route('/api/stats')
def api_stats():
	# figure out the different sizes of sets in the db
	query = "SELECT DISTINCT draw_size FROM bigset;"
	request = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
	results = request.json().get('data')
	print(results)
	
	stats = []
	for draw_size in results:
		# counts
		query = "SELECT COUNT(*) FROM bigset WHERE draw_size=%s;" % draw_size[0]
		result = requests.post('http://0.0.0.0:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		count = result.json().get('data')[0][0]

		# max sets in draw
		query = "SELECT MAX(num_sets) FROM bigset WHERE draw_size=%s;" % draw_size[0]
		result = requests.post('http://0.0.0.0:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		max_sets = result.json().get('data')[0][0]

		# totals sets in all draws
		query = "SELECT SUM(num_sets) FROM bigset WHERE draw_size=%s;" % draw_size[0]
		result = requests.post('http://0.0.0.0:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		total_sets = result.json().get('data')[0][0]

		# no sets in all draws
		query = "SELECT COUNT(*) FROM bigset WHERE draw_size=%s AND num_sets=0;" % draw_size[0]
		result = requests.post('http://0.0.0.0:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		no_sets = result.json().get('data')[0][0]

		stats.append({"draw_size": draw_size[0], "count": count, "max_sets": max_sets, "total_sets": total_sets, "no_sets": no_sets})
	

	return make_response(stats)


@app.route('/api/data')
def api_data():
	# draw size
	size = request.args.get('size')
	if not size:
		size = 12

	# data payload
	data = []

	# run a count range
	for num in range(0,24):
		query = "select count(*) from bigset where num_sets = %s and draw_size = %s;" % (num, size)

		result = requests.post('http://0.0.0.0:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})

		count = result.json().get('data')[0][0]

		if count != 0:
			data.append({"num_sets": num, "count": count})
			
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
	app.run(host='0.0.0.0', port=8000, debug=True)
	dev = True
