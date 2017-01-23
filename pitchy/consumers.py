from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user_from_http, channel_session_user
import json

from .models import Conversation

@channel_session
def ws_connect(message):
    #Accept the connection - this is needed for Channels 1.0 (but backward compatible fix in newer versions)
    message.reply_channel.send({"accept": True})

    #Get the conversation label from the url
    label = message['path'].strip('/')

    #Find the right conversation based on label
    room = Conversation.objects.get(label=label)

    #Hook to group/session based on label
    Group('chat-' + label).add(message.reply_channel)
    message.channel_session['room'] = room.label

@channel_session
def ws_receive(message):
    #Get label from session
    label = message.channel_session['room']

    #Find the right conversation based on label
    room = Conversation.objects.get(label=label)

    #Get message data from chat js
    data = json.loads(message['text'])

    #Create new message for given conversation using data
    m = room.messages.create(sender=data['sender'], body=data['body'])

    #Call save so that Conversation is registered as being updated (so updated_at will update)
    room.save()

    #Broadcast message to group
    Group('chat-'+label).send({'text': json.dumps(m.as_dict())})

@channel_session
def ws_disconnect(message):
    #Get current session
    label = message.channel_session['room']

    #Disconnect from group/websocket session
    Group('chat-'+label).discard(message.reply_channel)
