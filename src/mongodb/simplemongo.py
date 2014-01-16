__author__ = 'cocoon'

from datetime import datetime

import mongoengine
from mongoengine import *

class Message(Document):
    """
        the message collection schema
    """
    sequence= SequenceField()
    author = StringField(max_length=32)
    content= StringField(max_length=256)

    created = DateTimeField(default=datetime.now)

    meta = {
        'indexes': ['sequence' ],
        'ordering': ['sequence']
        }


class Mailbox(Document):
    """
        mailbox container for messages
    """
    # role : client or server
    role = StringField(max_length=16,required=True,choices=['CLIENT',"SERVER"])

    # kind: inbox or outbox
    kind = StringField(max_length=16,required=True,choices=['INBOX','OUTBOX'])

    # mode : PUSH PULL PASSIVE
    mode = StringField(max_length=16,required=True,choices=['ACTIVE','PASSIVE'])

    # bind: corresponding mailbox or None
    # Client Inbox  , mode PULL bind= http://server/mailbox/<id> , mode PUSH bind=None
    # Client Outbox , mode PUSH bind= http://server/mailbox/<id> , mode PULL bind = None
    # Server Inbox , bind=''
    # server Outbox , mode PUSH  bind= http//client/mailbox/<id> , else: None

    # url of corresponding remote mailbox url ( only usefull is this mailbox is in mode="ACTIVE"
    binding = StringField(default="")

    # messages
    messages = ListField(ReferenceField(Message))

    # actions: push , pull
    #actions = StringField(max_length=16)

    # parent session oid eg 52939114a2ecd0b829765bfc
    parent = StringField(max_length=32,default="")


    meta = {
        'indexes': ['mode','role' ]
        }


    # actions
    def push(self,content='blank message',author="anonymus"):
        """
            build a message from data , push it in messages array, return message

        """
        message= Message(author=author, content=content).save()
        self.messages.append(message)
        self.save()
        return message


    def pull(self,indice=0,save=True):
        """
            extract last (by_default) message from queue
            return message
        """
        message=self.messages.pop(indice)
        if save:
            self.save()
        return message





if __name__=="__main__":

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


