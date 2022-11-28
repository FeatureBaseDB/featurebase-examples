from featurebase import Client

# create client
client = Client('0.0.0.0:20101', auth=None)

query = client.querysql_future("create table test2  (_id id, int1 int);")
print(query.result())

"""
old = 0
for age in range(0,15):
  query = client.querysql_future("select count(*) from allyourbase where num_sets = %s;" % age)
  print(age, query.result())
  new = query.result()[0].get('count(*)')
  # print(float(old/new))
  old = new
"""


