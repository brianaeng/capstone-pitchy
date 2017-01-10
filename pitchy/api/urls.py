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
    # url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
    # url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    # url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    # url(r'^$', views.HomepageView.as_view(), name='homepage'),
    # url(r'^profile/edit/$', views.UpdateProfileView.as_view(), name='update_profile'),
    # url(r'^hub/$', views.HubView.as_view(), name='hub'),
    # url(r'^user/(?P<pk>\d+)/$', views.ProfileView.as_view(), name='profile'),
    # url(r'^messages/(?P<pk>\d+)/$', views.ConversationView.as_view(), name='messages'),
    # url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    # url(r'^post/new/$', views.post_new, name='post_new'),
    # url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
]
