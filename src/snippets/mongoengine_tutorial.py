from mongoengine import *
import datetime

connect('mdb')


class Page(Document):
    title = StringField(max_length=200, required=True)
    date_modified = DateTimeField(default=datetime.datetime.now)



