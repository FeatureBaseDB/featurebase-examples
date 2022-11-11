import json
import sys
import string
import random

from coolname import generate_slug
from bson import json_util

# import kafka and define producer
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='localhost:9093')

# random strings for IDs
def random_string(size=6, chars=string.ascii_letters + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

# schema
"""
[
	{
		"name": "user_id",
		"path": ["user_id"],
		"type": "string"
	},
	{
		"name": "name",
		"path": ["name"],
		"type": "string"
	},
	{
		"name": "age",
		"path": ["age"],
		"type": "id"
	}
]
"""

# insert 200,000 random entries
num = 200000
for x in range(num):
	data = {
		"user_id": random_string(size=8),
		"name": generate_slug(2),
		"age": random.randint(14,114)
	}
	out = producer.send('allyourbase', json.dumps(data, default=json_util.default).encode('utf-8'))

# flush the producer
producer.flush()

print("%s records inserted.")