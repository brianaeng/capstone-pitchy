from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'^$', views.HomepageView.as_view(), name='homepage'),
    url(r'^profile/edit/$', views.UpdateProfileView.as_view(), name='update_profile'),
    url(r'^connections/$', views.ConnectionsView.as_view(), name='connections'),
    url(r'^profiles/(?P<pk>\d+)/$', views.ProfileView.as_view(), name='profile'),
    url(r'^messages/(?P<pk>\d+)/$', views.ConversationView.as_view(), name='messages'),
    url(r'^friendship/confirm/(?P<pk>\d+)/', views.confirm_friend, name='confirmation'),
    url(r'^friendship/request/(?P<pk>\d+)/', views.request_friend, name='request_friend'),
    url(r'^search/$', views.search, name='search'),
    url(r'^new/$', views.new_room, name='new_room'),
    url(r'^(?P<label>\d+)/$', views.chat_room, name='chat_room'),
    # url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    # url(r'^post/new/$', views.post_new, name='post_new'),
    # url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
]
