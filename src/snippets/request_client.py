"""

    a rest client snippet fir requests


"""


import requests


base = "http://localhost:8088"

###
# create a client session
client = requests.Session()

# dont use proxy
client.trust_env = False

###


# request a  page
url = '/'
response = client.get( base + url)

# print status code
print response.status_code

# print content-type
print response.headers['content-type']



