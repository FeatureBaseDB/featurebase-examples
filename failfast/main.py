import json
import string
import random
import os, sys
import pickle

from bson import json_util

import config
import openai
import numpy as np

import database as featurebase

# get token
openai.api_key = config.openai_token

# gpt3 vectorization
def gpt3_embedding(content, engine='text-embedding-ada-002'):
	content = content.encode(encoding='ASCII',errors='ignore').decode()
	response = openai.Embedding.create(input=content,engine=engine)
	vector = response['data'][0]['embedding']  # this is a normal list
	return vector

# random strings for IDs
def random_string(size=6, chars=string.ascii_letters + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def search(text, fragments):
	return [fragment for fragment in fragments if fragment.get('text') == text]

featurebase.weaviate_delete("authorized", "All")

print(featurebase.weaviate_schema("pdf-schema.json"))

#######
# read the PDF
import PyPDF2

# creating a pdf file object
# pdfFileObj = open('faradayiii.pdf', 'rb')

pdfFileObj = open('pql.pdf', 'rb')

    
# creating a pdf reader object 
pdfReader = PyPDF2.PdfReader(pdfFileObj)
    
# printing number of pages in pdf file 
num_pages = len(pdfReader.pages)

# fragments
fragments = []

# creating a page object
page = 0
while True:
	try:
		pageObj = pdfReader.pages[page]
		page = page + 1

		_fragment = ""

		s = pageObj.extract_text()
		
		_line = ""
		for _s in s:
			_line = _line + _s
			if len(_line) > 250:
				featurebase.weaviate_update({"sentence": _line}, "PDF")
				_line = ""

	except Exception as ex:
		print(ex)
		break



# closing the pdf file object 
pdfFileObj.close() 

sys.exit()

for fragment in fragments:
	print(fragment)
	print("===============")
# sys.exit()

# add if we don't have it in the pickle
_id = len(fragments)
for fragment in fragments:
	if not search(fragment, pickled_fragments):
		pickled_fragments.append({"text": fragment, "_id": _id})
		_id = _id + 1

# build IDs and embeddings
for fragment in pickled_fragments:
	if fragment.get("name", '') == '':
		fragment.setdefault("name", random_string(4))
	if fragment.get("vector", []) == []:
		print("calling GPT-3")
		fragment.setdefault("vector", gpt3_embedding(fragment.get("text")))

# pseudo code
# insert fragment vector into weavite

# new fragment arrives
# embed
# search
for fragment in pickled_fragments:
	print(fragment.get("text"))
	print("==========================")


# compute dot products
fb_id = 0
for fragment_1 in pickled_fragments:
	for fragment_2 in pickled_fragments:
		if fragment_2.get("name") == fragment_1.get("name"):
			continue

		dot = np.dot(fragment_1.get("vector"), fragment_2.get("vector"))
		print(fragment_2.get("vector"))		
		data = {
			"_id": fb_id,
			"name_1": fragment_1.get("name"),
			"text_1": fragment_1.get("text"),
			"name_2": fragment_2.get("name"),
			"text_2": fragment_2.get("text"),
			"dot": "%s" % dot
		}
		# if float(data.get("dot")) > 851555879:
		#	print(fragment_1.get("text"), fragment_2.get("text"))
		

		print(data.get('text_1'), data.get('_id'), data.get("dot"), data.get('text_2'))
		fb_id = fb_id + 1

		# print(fragment_2.get("name"), fragment_1.get("name"))
		# print(np.dot(fragment_1.get("vector"), fragment_2.get("vector")))

pickle.dump(pickled_fragments, open("fragments.pickle", "wb"))
