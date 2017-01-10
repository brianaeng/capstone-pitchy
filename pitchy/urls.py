from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'^$', views.HomepageView.as_view(), name='homepage'),
    url(r'^profile/edit/$', views.UpdateProfileView.as_view(), name='update_profile'),
    url(r'^hub/$', views.HubView.as_view(), name='hub'),
    url(r'^user/(?P<pk>\d+)/$', views.ProfileView.as_view(), name='profile'),
    url(r'^messages/(?P<pk>\d+)/$', views.ConversationView.as_view(), name='messages'),
    url(r'^friendship/confirm/(?P<pk>\d+)/', views.confirm_friend, name='confirmation')
    # url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    # url(r'^post/new/$', views.post_new, name='post_new'),
    # url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
]
