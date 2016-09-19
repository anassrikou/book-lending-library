from django.conf.urls import url

from .views import (BookListView, BookDetailView, AddBookView, EditBookView, 
					DeleteBookView, UserListView, DeleteUserView, HomePageView, releasebook, Suggestions,
					Tagslist, AddTagView, EditTagView, DeleteTagView)

urlpatterns = [
	#homepage for staff
	url(r'^$', HomePageView.as_view(), name='homepage'),
	#books urls for staffs
	url(r'^books/$', BookListView.as_view(), name='book_list'),
	url(r'^books/add/$', AddBookView.as_view(), name='create'),
	url(r'^books/(?P<id>\d+)/$', BookDetailView.as_view(), name='detail'),
	url(r'^books/(?P<id>\d+)/edit/$', EditBookView.as_view(), name='update'),
	url(r'^books/(?P<id>\d+)/delete/$', DeleteBookView.as_view(), name='delete'),
	url(r'^books/(?P<id>\d+)/release/$', releasebook, name='release'),
	#users urls for staffs
	url(r'^users/$', UserListView.as_view(), name='user_list' ),
	url(r'^users/(?P<id>\d+)/delete/$', DeleteUserView.as_view(), name='delete_user'),
	url(r'^suggestions/$', Suggestions.as_view(), name='suggestions'),
	#tags url for staffs
	url(r'^tags/$', Tagslist.as_view(), name='tagslist'),
	url(r'^tags/add/$', AddTagView.as_view(), name='add_tag'),
	url(r'^tags/update/(?P<id>\d+)/$', EditTagView.as_view(), name='update_tag'),
	url(r'^tags/delete/(?P<id>\d+)/$', DeleteTagView.as_view(), name='delete_tag')
]