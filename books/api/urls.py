from django.conf.urls import url

from .views import BookViewSet

urlpatterns = [
	url(r'^$', BookViewSet.as_view(), name='book_list'),
]