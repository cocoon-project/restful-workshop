___author__ = 'cocoon'
"""
    stage 2 :

        use models.py for definition of Message

        test it

"""

import mongoengine

# import models from models.py
from models import Message , Mailbox


# define module variables
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


def test_mailbox():
    """

    """
    # connect to default mongod , base mdb
    mongoengine.connect(db_name)


    # create a mailbox
    mail = Mailbox( role = 'SERVER' , kind = 'INBOX' , mode = 'PASSIVE')
    # save it
    mail.save()

    # create a message and deposit in mailbox
    new_message = mail.push(content='my message to deposit', author = 'me')

    # dont forget to save
    mail.save()


    # show mailbox
    print "mailbox after message insertion"
    print mail.to_json()

    # print new message
    print "new_message inserted"
    print new_message.to_json()

    # extract message from mailbox
    me = mail.pull()
    mail.save()

    print "extract message"
    print me.to_json()

    # print mailbox after
    print "mailbox after message extraction"
    print mail.to_json()

    return

def test_invalid_mailbox_mode():
    """

    """
    # mode BIDON is incorrect ( see choices in model Mailbox )

    mail2=Mailbox(mode="BIDON",kind="INBOX",role="CLIENT" )

    try:
        mail2.save()
    except Exception,e:
        print e
    return


# begins here
test_message()
test_mailbox()
test_invalid_mailbox_mode()

print


