import weaviate
import config
import pprint

from database import weaviate_query
from ai import ai

client = weaviate.Client(
    url="http://localhost:8080",
    additional_headers={
        "X-OpenAI-Api-Key": config.openai_token
    }
)


# all_objects = client.data_object.get(class_name="PDF")
# print(all_objects)

sentences = []
for distance in range(20, 0, -1):
	query = "how do i get a count of different things?"
	print(float(distance/10))
	
	_sentences = weaviate_query({"concepts": query}, "PDF", float(distance/10))
	
	for sentence in _sentences:
		ss = sentence.get('sentence')
		# print(len(ss))
		sentences.append(ss)
		if len(sentences) > 10:
			break
	if len(sentences) > 10:
		break
#print(sentences)
answer = ai("read", {"sentences": sentences, "query": query})

print(query)
print(answer.get('explain'))

#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(answers)
