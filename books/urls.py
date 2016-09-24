from django.conf.urls import url

from .views import BookListView, BookDetailView, bookborrow, SuggestBookView

urlpatterns = [
	url(r'^$', BookListView.as_view(), name='list'),
	url(r'^(?P<id>\d+)/$', BookDetailView.as_view(), name='detail'),
	url(r'^(?P<id>\d+)/borrow/$', bookborrow, name='borrow'),
	url(r'^suggestbook/$', SuggestBookView.as_view(), name='suggestbook'),
]