import os
import sys
import datetime
import random
import openai

import traceback

from string import Template

from database import weaviate_query

import config

# AI model call by method name
models = {}
model = lambda f: models.setdefault(f.__name__, f)

def ai(model_name="none", document={}):
	# get the user's API token	
	openai_token = config.openai_token

	if not openai_token:
		# rewrite to match document flow
		document['error'] = "model %s errors with no token." % (model_name)
		document['explain'] = "I encountered an error talking with OpenAI."
		document['template_file'] = "eject_document"
		return document
	else:
		# set token for model to use
		document['openai_token'] = openai_token

	# call the model
	try:
		document = models[model_name](document)
		return document

	except Exception as ex:
		if config.dev == "True":
			print("MMMMMM")
			print(traceback.format_exc())

		document['error'] = "model %s errors with no token." % (model_name)
		document['explain'] = "I encountered an error talking with my AI handler."
		document['template_file'] = "eject_document"
		return document


# helper functions
# ================

# load template
def load_template(name="default"):
	# file path
	lib_path = os.path.dirname(__file__)
	file_path = "templates/%s.txt" % name

	try:
		with open(file_path, 'r') as f:
			template = Template(f.read())
	except Exception as ex:
		print(ex)
		print("exception in loading template")
		template = None

	return template


# gpt3 dense vectors
def gpt3_embedding(content, engine='text-similarity-ada-001'):
	content = content.encode(encoding='ASCII',errors='ignore').decode()
	response = openai.Embedding.create(input=content,engine=engine)
	vector = response['data'][0]['embedding']  # this is a normal list
	return vector


# completion
def gpt3_completion(prompt, temperature=0.95, max_tokens=256, top_p=1, fp=0, pp=0):
	try:
		# call to OpenAI completions
		response = openai.Completion.create(
		  model = "text-davinci-003",
		  prompt = prompt,
		  temperature = temperature,
		  max_tokens = max_tokens,
		  top_p = top_p,
		  frequency_penalty = fp,
		  presence_penalty = pp
		)

		answer = response['choices'][0]['text']
	except Exception as ex:
		answer = "Call to OpenAI completion failed: %s" % ex

	return answer


# model functions
# ===============

# dream an image
@model
def dream(document):
	# load openai key then drop it from the document
	openai.api_key = document.get('openai_token')
	document.pop('openai_token', None)
	
	response = openai.Image.create(
	    prompt=document.get('plain'),
	    n=1,
	    size="256x256",
	)

	url = response["data"][0]["url"]
	
	return url


# not in use
@model
def read(document, template_file="read"):
	# load openai key then drop it from the document
	openai.api_key = document.get('openai_token')
	document.pop('openai_token', None)

	template = load_template(template_file)

	# no substitutions for this template, yet
	prompt = template.substitute(document)

	document['explain'] = gpt3_completion(prompt, temperature=0.85, max_tokens=256).strip("\n")
	return document


# uses templates in templates directory
# set template using document key "template_file"
# use of "eject_document" will force a reply to Discord
@model
def query(document):
	# load openai key then drop it from the document
	openai.api_key = document.get('openai_token')
	document.pop('openai_token', None)

	# get the template file to use
	template_file = document.get('template_file', "determine_intent")

	# random number for ids
	document['random'] = int(random.random()*1000000000)
	for distance in range(0, 10):
		intents = weaviate_query({"concepts": [document.get('plain')]}, "Intent", float(distance/10))

		if len(intents) > 5:
			break

	_intents = []
	for intent in intents:
		intent.pop('_additional')
		_intents.append(intent)

	document['intents'] = _intents

	# substitute things
	template = load_template(template_file)
	prompt = template.substitute(document)

	# ask GPT-3 for an answer
	answer = gpt3_completion(prompt)

	# try to eval the result
	try:
		# prepend the completion with a dictionary {
		answer_dict = eval('{%s' % (answer.strip("\n").strip(" ").replace("\n", "")))
		document = {**document, **answer_dict}

	# we failed to eval
	except Exception as ex:
		# bad sql
		exc_type, exc_obj, exc_tb = sys.exc_info()
		print("=============EVAL==============")
		print(exc_type, exc_obj, exc_tb)
		print(ex)
		print(answer)
		print("===============================")
		if not document.get('explain', None):
			document['explain'] = "I had problems returning a valid response."

		document['error'] = ex
	
		document['is_sql'] = False
		document['template_file'] = "eject_document"

	return document


# not in use, yet
@model
def feedback(document, template_file="sql_feedback"):
	openai.api_key = document.get('openai_token')

	prompt_data = {
		"plain": document.get('plain'),
		"author": document.get('author'),
		"tables": document.get('tables'),
		"error": document.get('error'),
		"sql": document.get('sql'),
		"rand_number": int(random.random()*1000000000)
	}

	template = load_template(template_file)
	prompt = template.substitute(prompt_data)

	answer = gpt3_completion(prompt)

	try:
		answer_dict = eval('{%s' % (answer.strip("\n").strip(" ")))
	except:
		print("Exception with eval'ing answer!")
		print("===============================")
		answer_dict = {"explain": "I had problems building a response.", "is_sql": "False"}

	return answer_dict
