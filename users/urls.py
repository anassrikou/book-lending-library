from django.conf.urls import url

from .views import  profile, update
from django.contrib.auth.views import password_change

urlpatterns = [
	url(r'^profile/resetpassword/$', password_change, name='reset_password'),
    url(r'^profile/(?P<id>\d+)/$', profile, name='profile'),
    url(r'^update_profile/(?P<id>\d+)/$', update, name='update'),
]