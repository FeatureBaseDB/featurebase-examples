import datetime
import logging
import os, sys
import json

import requests

from flask import Flask
from flask import session, request, redirect
from flask import render_template, make_response
from flask import url_for

from sets import generate

# app up
app = Flask(__name__)

#@app.route('/')
#def index():
#    return render_template('index.html')

@app.route('/sets')
def sets():
    return render_template('sets.html')

@app.route('/draws')
def draws():
	return render_template('draws.html')

@app.route('/cards')
def cards():
	return render_template('cards.html')

@app.route('/')
def dashboard():
	return render_template('dashboard.html')

@app.route('/api/generate')
def api_generate():
	# get the number of entries
	query = "select count(*) from bigset;"
	result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
	num_records = result.json().get('data')[0][0]

	size = request.args.get('size')
	if not size:
		size = 12

	num_sets = request.args.get('num')
	if not num_sets:
		num_sets = 10000

	generate(size, num_sets, num_records, cluster_port)

	return make_response({"result": "complete"})

@app.route('/api/draw')
def api_draw():
	# draw size
	num_sets = request.args.get('num')
	if not num_sets:
		num_sets = 0

	# draw size
	size = request.args.get('size')
	if not size:
		size = 12

	query = "select draw from bigset where draw_size=%s and num_sets=%s;" % (size, num_sets)
	result = requests.post('http://0.0.0.0:10101/sql', data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
	print(result.text)
	data = result.json().get('data')[0][0]
	
	return make_response(data)

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

@app.route('/api/stats')
def api_stats():
	query = "select "
	pass

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
		print(query)
		result = requests.post('http://0.0.0.0:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		print(result.text)
		count = result.json().get('data')[0][0]

		if count != 0:
			data.append({"num_sets": num, "count": count})
		
	return make_response(data)

if __name__ == '__main__':
	"""
	try:
		query = "[bigset]Rows(draw_size)"
		result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
	except:
		print("yeah, no")
		sys.exit()

	"""
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

	try:
		query = "select count(*) from bigset;"
		result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		num_records = result.json().get('data')[0][0]
	except:
		query = "create table bigset (_id id, draw idset, sets idset, num_sets int, draw_size int);"
		result = requests.post('http://localhost:%s/sql' % cluster_port, data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})

	# This is used when running locally.
	# app.run(host='127.0.0.1', port=8000, debug=True)
	app.run(host='0.0.0.0', port=8000, debug=True)
	dev = True
