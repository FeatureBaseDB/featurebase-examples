import requests
import json
import config

def auth():
	data = {
		"USERNAME": config.username,
		"PASSWORD": config.password
	}
	result = requests.post(
		'https://id.featurebase.com',
		json.dumps(data)
	)
	return json.loads(result.text)

# grab the token
fb_auth = auth()
id_token = fb_auth.get('AuthenticationResult').get('IdToken')


# run a query
headers = {'Authorization': 'Bearer %s' % id_token, 'Content-Type': 'text/plain'}
endpoint = "https://query.featurebase.com/v2/databases/a0740414-1872-4ddd-8961-ceafcd44db86/query/sql"

result = requests.post(
	endpoint,
	data = "SELECT DISTINCT ip_address FROM fb_metrics;",
	headers=headers
).json()

ips = result.get('data')

'''
for ip in ips:
	query = "SELECT COUNT(*) FROM fb_metrics WHERE ip_address = '%s'" % ip[0]

	result = requests.post(
		endpoint,
		data = query,
		headers=headers
	).json()
	print(ip, result.get('data')[0][0])
'''

for ip in ips:
	query = "SELECT COUNT(DISTINCT client_id) FROM fb_metrics WHERE ip_address = '%s'" % ip[0]

	result = requests.post(
		endpoint,
		data = query,
		headers=headers
	).json()
	print(ip, result.get('data')[0][0])