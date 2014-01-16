__author__ = 'cocoon'

import mongoengine


from models import *

#default database name
db_name = "mdb"


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
          note the exclude , dont show _id of messages
    """
    messages = Message.objects().exclude('id')
    for message in messages:
        print message.to_json()


def show_messages_from(author_name):
    """

    """
    messages = Message.objects(author=author_name).all()
    for message in messages:
        print message.to_json()

