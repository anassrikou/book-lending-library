from django.conf.urls import url

from .views import BookListView, BookDetailView, bookborrow

urlpatterns = [
	url(r'^$', BookListView.as_view(), name='list'),
	url(r'^(?P<id>\d+)/$', BookDetailView.as_view(), name='detail'),
	url(r'^(?P<id>\d+)/borrow/$', bookborrow, name='borrow'),
]