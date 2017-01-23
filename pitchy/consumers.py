from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user_from_http, channel_session_user
import json

from .models import Conversation

@channel_session
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    label = message['path'].strip('/')
    room = Conversation.objects.get(label=label)
    Group('chat-' + label).add(message.reply_channel)
    message.channel_session['room'] = room.label

@channel_session
def ws_receive(message):
    label = message.channel_session['room']
    room = Conversation.objects.get(label=label)
    data = json.loads(message['text'])
    m = room.messages.create(sender=data['sender'], body=data['body'])
    room.save()
    Group('chat-'+label).send({'text': json.dumps(m.as_dict())})

@channel_session
def ws_disconnect(message):
    label = message.channel_session['room']
    Group('chat-'+label).discard(message.reply_channel)
