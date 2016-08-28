from django.conf.urls import url

from .views import (BookListView, BookDetailView, AddBookView, EditBookView, 
					DeleteBookView, UserListView, DeleteUserView, HomePageView, releasebook)

urlpatterns = [
	#homepage for staff
	url(r'^$', HomePageView.as_view(), name='homepage'),
	#books urls for staffs
	url(r'^books/$', BookListView.as_view(), name='list'),
	url(r'^add/$', AddBookView.as_view(), name='create'),
	url(r'^books/(?P<id>\d+)/$', BookDetailView.as_view(), name='detail'),
	url(r'^books/(?P<id>\d+)/edit/$', EditBookView.as_view(), name='update'),
	url(r'^books/(?P<id>\d+)/delete/$', DeleteBookView.as_view(), name='delete'),
	url(r'^books/(?P<id>\d+)/release/$', releasebook, name='release'),
	#users urls for staffs
	url(r'^users/$', UserListView.as_view(), name='user_list' ),
	url(r'^users/(?P<id>\d+)/delete/$', DeleteUserView.as_view(), name='delete_user'),
]