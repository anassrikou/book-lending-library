from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from books.models import Book
from books.forms import BookForm, BookBorrowForm

class HomePageView(TemplateView):
	# def dispatch(self, request, *args, **kwargs):
	# 	try:
	# 		request.user.groups.get(name="user")
	# 	except:
	# 		return render(request, "no_access.html")
	# 	# try request.user.groups.get(name="user"):
	# 	# 	return render(request, 'staff_homepage.html')
	# 	# else:
	# 	# 	raise PermissionDenied
	# 	return super(HomePageView, self).dispatch(request, *args, **kwargs)
	template_name = "staff_homepage.html"


""" Book CRUD """
#list all books
class BookListView(ListView):
	def get(self, request):
		books = Book.objects.all()
		query = request.GET.get("q")
		if query:
			books = books.filter(
			Q(book_name__icontains=query)|
			Q(author_name__icontains=query)|
			Q(tags__name__icontains=query)
			).distinct()

		paginator = Paginator(books, 10) # Show 25 contacts per page

		page = request.GET.get('page')
		try:
			books = paginator.page(page)
		except PageNotAnInteger:
		# If page is not an integer, deliver first page.
			books = paginator.page(1)
		except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
			books = paginator.page(paginator.num_pages)
		
		context = {
			'books' : books,
			}
		return render(request, 'staff_book_list.html', context)

#list detail for specific book
class BookDetailView(DetailView):
	model = Book
	pk_url_kwarg = 'id'
	template_name = "book_detail.html"

#Create new book
class AddBookView(CreateView):
	form_class = BookForm
	model = Book
	template_name = "staff_add_book.html"

	def get_success_url(self):
		return reverse('staff:detail', kwargs={'id' : self.object.id})

#Update/modify a specific book
class EditBookView(UpdateView):
	form_class = BookForm
	model = Book
	template_name = "staff_add_book.html"
	pk_url_kwarg = 'id'

	def get_success_url(self):
		return reverse('staff:detail', kwargs={'id' : self.object.id})

#delete a specific book
class DeleteBookView(DeleteView):
	model = Book
	template_name = "confirm_delete.html"
	pk_url_kwarg = 'id'

	def get_success_url(self):
		return reverse('staff:list')

#release book from user
def releasebook(request, id):
	book = get_object_or_404(Book, id=id)
	if request.method == "POST":
		book.status = True
		book.borrower = None
		book.save()
	return redirect(reverse('staff:list'))

""" User CRUD """

#list all the users
class UserListView(ListView):
	def get(self, request):
		users = User.objects.all()
		context = {
			'users' : users
		}
		return render(request, 'staff_user_list.html', context)

#delete a specific user
class DeleteUserView(DeleteView):
	model = User
	template_name = "confirm_delete.html"
	pk_url_kwarg = 'id'

	def get_success_url(self):
		return reverse('staff:user_list')