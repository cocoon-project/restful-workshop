__author__ = 'cocoon'
"""
    stage 0 :

        define a model for a Message document

        define some functions to test it

        test it

"""

#from datetime import datetime

import mongoengine
from mongoengine import Document, StringField


# model definition
class Message(Document):
    """
        the message collection schema
    """

    # define author fields
    author = StringField(max_length=32)

    # define content field : text of message
    content= StringField(max_length=256)


#
# variables definitions
#

# the database name
db_name="mdb"

#
# functions
#
def connect_to_mongodb(name=db_name):
    """
        dont forget to start mongod daemon !

    """
    # connect to default mongod , base mdb
    mongoengine.connect(name)


def raz(name=db_name):
    """
        drop all collections from mdb database
    """
    #get current connection to mongod
    db = mongoengine.connection._get_db()
    #drop all collections from db_name
    db.connection.drop_database(name)


def show_messages():
    """
        show all messages
          note the exclude
    """
    messages = Message.objects()
    for message in messages:
        print message.to_json()


def test_message():


    # create one message explict
    m1 = Message(author="me",content="hello")
    m1.save()


    # show all messages
    print "all messages"
    show_messages()

    return



#######################################
# begins here

# connect to mongodb
connect_to_mongodb()

# drop all collections from mdb database
raz()

# test create message
test_message()


print "exit"



