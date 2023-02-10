import sys
import weaviate
import random
import string

import requests
from string import Template

import config

# parse helper
def find_between(s, first, last):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

# random strings
def random_string(size=6, chars=string.ascii_letters + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

###############
# FeatureBase #
###############

def featurebase_tables_schema(table_name=None):
	# get current tables
	if not table_name:
		index_url = "%s/index" % config.featurebase_url
	else:
		index_url = "%s/index/%s" % (config.featurebase_url, table_name)

	try:
		# get the index information
		result = requests.get(index_url)

		# toggle on one or many
		if table_name:
			_result = [result.json()]
		else:
			_result = result.json().get("indexes")

		# table array
		tables = []

		# iterrate on results to build tables, schemas and create sequences
		for table in _result:
			if table.get('name', 'fb_views') != "fb_views":
				# sql endpoint
				query_url = "%s/sql" % config.featurebase_url

				# query to get create table statement
				query = "SHOW CREATE TABLE %s;" % table.get('name')
				
				# run a query
				result = requests.post(
					query_url,
					data=query.encode('utf-8'),
					headers={'Content-Type': 'text/plain'}
				).json()

				# grab the data from the response
				data = result.get('data')[0][0]
				schema = find_between(data, "(", ")")

				# build fields
				fields = []
				for field in schema.split(","):
					field = field.strip(" ")
					field_name = field.split(" ")[0]
					field_type = field.split(" ")[1]
					fields.append(
						{
							"name": field_name,
							"type": field_type
						}
					)

				# prep entry to array
				entry = {
					"name": table.get('name'),
					"fields": fields,
					"create_table_sql": data
				}

				# append to table array
				tables.append(entry)

	except Exception as ex:
		# something went wrong, so return nothing
		tables = None
		print(ex)

	return tables

# build a list of the current tables in a string
def featurebase_tables_string(table_name=None):
	# get the full table list + schema
	tables = featurebase_tables_schema(table_name)
	
	# if there were no tables, or no connection, return
	if not tables:
		return None

	# build a string of the table names with commas
	_table_string = ""
	for table in tables:
		if table.get('name', 'fb_views') != "fb_views":
			_table_string = _table_string + " " + table.get('name') + ","
	
	return _table_string.strip(",").strip(" ")


# query featurebase by document
# "sql" key in document should have a valid query
def featurebase_query(document):
	# try to run the query
	try:
		# we only need the SQL
		query = document.get("sql")
		result = requests.post(
			config.featurebase_url+"/sql",
			data=query.encode('utf-8'),
			headers={'Content-Type': 'text/plain'}
		).json()
		print(result.get('data'))
		# add data to document to return

	except Exception as ex:
		# bad query?
		exc_type, exc_obj, exc_tb = sys.exc_info()
		print("=============")
		print(exc_type, exc_obj, exc_tb)
		print("=============")
	
	return document

############
# Weaviate #
############

# connect to weaviate
weaviate_client = weaviate.Client(config.weaviate_url)

# query weaviate for matches
def weaviate_query(document, collection, distance=0.5):
	nearText = {
	  "concepts": document.get('concepts'),
	  "distance": distance,
	}

	# fetch result and fields
	result = (
	  weaviate_client.query
	  .get(collection, ["sentence"])
	  .with_additional(["certainty", "distance", "id"])
	  .with_near_text(nearText)
	  .do()
	)

	_records = []

	for record in result.get('data').get('Get').get(collection):
		_records.append(record)

	return _records

# send a document to a class/collection
def weaviate_update(document, collection):
	try:
		data_uuid = weaviate_client.data_object.create(document, collection)

	except Exception as ex:
		print(ex)
		data_uuid = False

	return data_uuid

def weaviate_delete(uuid, collection):

	if collection == "All" and uuid == "authorized":
		# wipe the entire thing
		weaviate_client.schema.delete_all()
		return

	# delete the document
	try:
		weaviate_client.data_object.delete(uuid, collection)
	except Exception as ex:
		print(ex)

	return {"uuid": uuid}

def weaviate_schema(filename="weaviate_schema.json"):
	# connect to weaviate and ensure schema exists
	try:
		weaviate_client = weaviate.Client("http://localhost:8080")

		# Need to reset Weaviate?
		# weaviate_client.schema.delete_all()

		# make schemas if none found
		if not weaviate_client.schema.contains():
			dir_path = os.path.dirname(os.path.realpath(__file__))
			schema_file = os.path.join(dir_path, "schema/%s" % filename)
			print(schema_file)

			weaviate_client.schema.create(schema_file)

	except Exception as ex:
		print(ex)

	return({"filename": filename})

