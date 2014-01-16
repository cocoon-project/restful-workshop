__author__ = 'cocoon'
"""
    stage 2 :

        use models.py for definition of Message

        test it

"""

import mongoengine

# import models from models.py
from models import Message



db_name="mdb"


messages=[
    { 'author':"me", 'content':"hello from me"},
    { 'author':"me", 'content':"bye from me"},
    { 'author':"you", 'content':"hello from you"},
    { 'author':"you", 'content':"bye from you"},
]


def raz(db_name):
    """
        drop all collections from mdb database
    """
    #get current connection to mongod
    db = mongoengine.connection._get_db()
    #drop all collections from db_name
    db.connection.drop_database(db_name)


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



def test_message():

    # connect to default mongod , base mdb
    mongoengine.connect(db_name)

    # drop all collections from mdb database
    raz(db_name)

    # create one message explict
    m1 = Message(author="me",content="hello")
    m1.save()

    # create one message from messages list
    m2_data = messages[1]
    m2 = Message(author=m2_data['author'],content=m2_data['content'])
    m2.save()

    # create multiple messages from messages list
    for m_data in messages[2:]:
        m = Message(author=m_data['author'],content=m_data['content'])
        m.save()

    # show all messages
    print "all messages"
    show_messages()

    # show my messages
    print "my messages"
    show_messages_from("me")

    return




# begins here
test_message()


print "exit"



