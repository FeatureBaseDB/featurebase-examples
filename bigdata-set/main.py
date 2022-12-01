import datetime
import logging
import os
import json

import requests

from flask import Flask
from flask import session, request, redirect
from flask import render_template, make_response
from flask import url_for

# app up
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sets')
def sets():
    return render_template('sets.html')

@app.route('/cardss')
def cardss():
	return render_template('cards.html')

@app.route('/draw')
def draw():
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

@app.route('/cards')
def cards():
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
		result = requests.post('http://0.0.0.0:10101/sql', data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		print(result.text)
		count = result.json().get('data')[0][0]

		if count != 0:
			data.append({"cards": num, "count": count})
		
	return make_response(data)

@app.route('/data')
def data():
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
		result = requests.post('http://0.0.0.0:10101/sql', data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
		print(result.text)
		count = result.json().get('data')[0][0]

		if count != 0:
			data.append({"num_sets": num, "count": count})
		
	return make_response(data)

if __name__ == '__main__':
	# This is used when running locally.
	# app.run(host='127.0.0.1', port=8000, debug=True)
	app.run(host='0.0.0.0', port=8000, debug=True)
	dev = True