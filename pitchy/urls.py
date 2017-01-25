from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'^$', views.HomepageView.as_view(), name='homepage'),
    url(r'^connections/$', views.ConnectionsView.as_view(), name='connections'),
    url(r'^profile/edit/$', views.UpdateProfileView.as_view(), name='update_profile'),
    url(r'^profile/(?P<pk>\d+)/$', views.ProfileView.as_view(), name='profile'),
    url(r'^focus/(?P<pk>\d+)/$', views.focus_users, name='focus_users'),
    url(r'^friendship/confirm/(?P<pk>\d+)/', views.confirm_friend, name='confirmation'),
    url(r'^friendship/reject/(?P<pk>\d+)/', views.reject_friend, name='rejection'),
    url(r'^friendship/request/(?P<pk>\d+)/', views.request_friend, name='request_friend'),
    url(r'^friendship/delete/(?P<pk>\d+)/', views.delete_friend, name='delete_friend'),
    url(r'^search/$', views.search, name='search'),
    url(r'^messages/$', views.recent_messages, name='messages'),
    url(r'^new_chat/(?P<pk>\d+)', views.start_chat, name='new_chat'),
    url(r'^create_chat/$', views.CreateChatView.as_view(), name='create_chat'),
    url(r'^(?P<label>[A-Za-z0-9\-\_]+)/$', views.chat_room, name='chat')
]
