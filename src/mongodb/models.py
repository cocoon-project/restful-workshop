__author__ = 'cocoon'

from datetime import datetime

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
