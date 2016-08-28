from django.conf.urls import url

from .views import BookListView, BookDetailView, AddBookView, EditBookView, DeleteBookView, BorrowBookView

urlpatterns = [
	url(r'^$', BookListView.as_view(), name='list'),
	url(r'^add/$', AddBookView.as_view(), name='create'),
	url(r'^(?P<id>\d+)/$', BookDetailView.as_view(), name='detail'),
	url(r'^(?P<id>\d+)/edit/$', EditBookView.as_view(), name='update'),
	url(r'^(?P<id>\d+)/delete/$', DeleteBookView.as_view(), name='delete'),
	url(r'^(?P<id>\d+)/borrow/$', BorrowBookView.as_view(), name='borrow'),
]