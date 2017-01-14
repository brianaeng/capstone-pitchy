from channels.staticfiles import StaticFilesConsumer
from . import consumers

channel_routing = {
    # This makes Django serve static files from settings.STATIC_URL, similar
    # to django.views.static.serve. This isn't ideal (not exactly production
    # quality) but it works for a minimal example.
    'http.request': StaticFilesConsumer(),

    # Wire up websocket channels to our consumers:
    'websocket.connect': consumers.ws_connect,
    'websocket.receive': consumers.ws_receive,
    'websocket.disconnect': consumers.ws_disconnect,
}

# from channels import route
# from .consumers import ws_connect, ws_receive, ws_disconnect
#
# # There's no path matching on these routes; we just rely on the matching
# # from the top-level routing. We _could_ path match here if we wanted.
# websocket_routing = [
#     # Called when WebSockets connect
#     route("websocket.connect", ws_connect),
#
#     # Called when WebSockets get sent a data frame
#     route("websocket.receive", ws_receive),
#
#     # Called when WebSockets disconnect
#     route("websocket.disconnect", ws_disconnect),
# ]
