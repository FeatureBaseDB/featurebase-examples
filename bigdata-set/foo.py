import requests
num = 0
size = 12
query = "select count(*) from bigset where num_sets = %s and draw_size = %s;" % (num, size)
print(query)
result = requests.post('http://0.0.0.0:10101/sql', data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
print(result.text)
query = "select count(num_sets) from bigset where num_sets = %s and draw_size = %s;" % (num, size)
print(query)
result = requests.post('http://0.0.0.0:10101/sql', data=query.encode('utf-8'), headers={'Content-Type': 'text/plain'})
print(result.text)
