from django.conf.urls import url

from .views import  profile
from django.contrib.auth.views import password_change

urlpatterns = [
	url(r'^profile/resetpassword/$', password_change, name='reset_password'),
    url(r'^profile/(?P<id>\d+)/$', profile, name='profile'),
]