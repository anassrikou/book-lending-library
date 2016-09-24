from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^u/$', views.UserViewSet.as_view()),
    url(r'^g/$', views.GroupViewSet.as_view()),
]