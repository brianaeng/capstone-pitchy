# import re
# import json
# import logging
# from channels import Group
# from channels.sessions import channel_session
# from .models import Conversation
#
# log = logging.getLogger(__name__)
#
# @channel_session
# def ws_connect(message):
#     # Extract the room from the message. This expects message.path to be of the
#     # form /chat/{label}/, and finds a Room if the message path is applicable,
#     # and if the Room exists. Otherwise, bails (meaning this is a some othersort
#     # of websocket). So, this is effectively a version of _get_object_or_404.
#     try:
#         prefix, label = message['path'].decode('ascii').strip('/').split('/')
#         if prefix != 'chat':
#             log.debug('invalid ws path=%s', message['path'])
#             return
#         room = Conversation.objects.get(label=label)
#     except ValueError:
#         log.debug('invalid ws path=%s', message['path'])
#         return
#     except Conversation.DoesNotExist:
#         log.debug('ws room does not exist label=%s', label)
#         return
#
#     log.debug('chat connect room=%s client=%s:%s',
#         room.label, message['client'][0], message['client'][1])
#
#     # Need to be explicit about the channel layer so that testability works
#     # This may be a FIXME?
#     Group('chat-'+label, channel_layer=message.channel_layer).add(message.reply_channel)
#
#     message.channel_session['room'] = room.label
#
# @channel_session
# def ws_receive(message):
#     # Look up the room from the channel session, bailing if it doesn't exist
#     try:
#         label = message.channel_session['room']
#         room = Conversation.objects.get(label=label)
#     except KeyError:
#         log.debug('no room in channel_session')
#         return
#     except Conversation.DoesNotExist:
#         log.debug('recieved message, buy room does not exist label=%s', label)
#         return
#
#     # Parse out a chat message from the content text, bailing if it doesn't
#     # conform to the expected message format.
#     try:
#         data = json.loads(message['text'])
#     except ValueError:
#         log.debug("ws message isn't json text=%s", text)
#         return
#
#     if set(data.keys()) != set(('handle', 'message')):
#         log.debug("ws message unexpected format data=%s", data)
#         return
#
#     if data:
#         log.debug('chat message room=%s handle=%s message=%s',
#             room.label, data['handle'], data['message'])
#         m = room.messages.create(**data)
#
#         # See above for the note about Group
#         Group('chat-'+label, channel_layer=message.channel_layer).send({'text': json.dumps(m.as_dict())})
#
# @channel_session
# def ws_disconnect(message):
#     try:
#         label = message.channel_session['room']
#         room = Conversation.objects.get(label=label)
#         Group('chat-'+label, channel_layer=message.channel_layer).discard(message.reply_channel)
#     except (KeyError, Room.DoesNotExist):
#         pass


from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user_from_http, channel_session_user
import json

from .models import Conversation

# @channel_session_user_from_http
@channel_session
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    prefix, label = message['path'].strip('/').split('/')
    room = Conversation.objects.get(label=label)
    Group('chat-' + label).add(message.reply_channel)
    message.channel_session['room'] = room.label

@channel_session
def ws_receive(message):
    label = message.channel_session['room']
    room = Conversation.objects.get(label=label)
    data = json.loads(message['text'])
    m = room.messages.create(sender=data['sender'], body=data['body'])
    Group('chat-'+label).send({'text': json.dumps(m.as_dict())})

# @channel_session_user
@channel_session
def ws_disconnect(message):
    label = message.channel_session['room']
    Group('chat-'+label).discard(message.reply_channel)
