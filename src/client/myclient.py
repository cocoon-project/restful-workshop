"""

    client to acces recipes-apy.py


"""


import requests


base = "http://localhost:8088/"

# get recipes
r = requests.get( base + 'recipes/')

# print status code
print r.status_code

# print content-type
print r.headers['content-type']

# convert json response to var
recipes =r.json()

# print all recipes
print recipes

# get the first recipe
first_recipe = recipes['paths'][0]


# fetch the first recipe
r = requests.get( base + 'recipes/' + first_recipe )

# print status code
print r.status_code

# print content-type
print r.headers['content-type']

# print the xml text received
print r.text


print


