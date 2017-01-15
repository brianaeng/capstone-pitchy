from django.conf.urls import url
# from . import views
# from django.contrib.auth import views as auth_views
from .views import FocusListAPIView, ProfileListAPIView, FriendshipListAPIView, FriendRequestListAPIView, ConversationListAPIView, DirectMessageListAPIView, ProfileViewSet, CreateUserAPIView, CreateProfileAPIView, CreateConversationAPIView, CreateDirectMessageAPIView, UserSearchAPIView

profile_detail = ProfileViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
})

urlpatterns = [
#GET
    url(r'^focuses/$', FocusListAPIView.as_view(), name='focuses'), #api/pitchy/focuses/
    url(r'^users/$', ProfileListAPIView.as_view(), name='users'), #api/pitchy/users
    url(r'^friendships/$', FriendshipListAPIView.as_view(), name='friendships'), #api/pitchy/friendships
    url(r'^friendshiprequests/$', FriendRequestListAPIView.as_view(), name='friendrequests'), #api/pitchy/friendrequests
    url(r'^conversations/$', ConversationListAPIView.as_view(), name='conversations'), #api/pitchy/conversations
    url(r'^conversations/(?P<pk>\d+)/messages/$', DirectMessageListAPIView.as_view(), name='messages'), #api/pitchy/conversations/ID/messages
#CREATE
    url(r'^users/new/$', CreateUserAPIView.as_view(), name='newuser'),
    url(r'^profile/new/$', CreateProfileAPIView.as_view(), name='newprofile'),
    url(r'^conversation/new/$', CreateConversationAPIView.as_view(), name='newconversation'),
    url(r'^message/new/$', CreateDirectMessageAPIView.as_view(), name='newdirectmessage'),
#SET (GET/PUT)
    url(r'^users/(?P<pk>\d+)/$', profile_detail, name='userdetails'),
    url(r'^$', UserSearchAPIView.as_view(), name='usersearch'),
]
