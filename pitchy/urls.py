from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomepageView.as_view(), name='homepage'),
    url(r'^profile/edit/$', views.UpdateProfileView.as_view(), name='update_profile'),
    url(r'^hub/$', views.HubView.as_view(), name='hub'),
    url(r'^user/(?P<pk>\d+)/$', views.ProfileView.as_view(), name='profile'),
    # url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    # url(r'^post/new/$', views.post_new, name='post_new'),
    # url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
]
