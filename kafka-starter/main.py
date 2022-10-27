import json
import sys
from bson import json_util

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

def on_success(record):
    print(record.topic)
    print(record.partition)
    print(record.offset)

def on_error(excp):
    log.error(excp)
    raise Exception(excp)


data = {"user_id" : "1a", "name" : "joe", "age" : 30}
	
producer.send('steve', json.dumps(data, default=json_util.default).encode('utf-8')).add_callback(on_success).add_errback(on_error)

producer.flush()
