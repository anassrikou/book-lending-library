from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse
from stronghold.views import StrongholdPublicMixin

from django.contrib.auth.models import User

from books.models import Book, BookSuggestion, Tags
from books.forms import BookForm, BookBorrowForm, TagsForm

class HomePageView(TemplateView):
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
class AddBookView(SuccessMessageMixin, CreateView):
	form_class = BookForm
	model = Book
	template_name = "staff_add_form.html"
	success_message = "%(book_name)s was created successfully"

	def get_context_data(self, **kwargs):
		context = super(AddBookView, self).get_context_data(**kwargs)
		context.update({'pagename': "Add new Book"})
		return context

	def get_success_url(self):
		return reverse('staff:book_list')

#Update/modify a specific book
class EditBookView(SuccessMessageMixin, UpdateView):
	form_class = BookForm
	model = Book
	template_name = "staff_add_form.html"
	pk_url_kwarg = 'id'
	success_message = "%(book_name)s was updated successfully"

	def get_context_data(self, **kwargs):
		context = super(EditBookView, self).get_context_data(**kwargs)
		context.update({'pagename': "Update Book"})
		return context

	def get_success_url(self):
		return reverse('staff:book_list')

#delete a specific book
class DeleteBookView(SuccessMessageMixin, DeleteView):
	model = Book
	template_name = "confirm_delete.html"
	pk_url_kwarg = 'id'
	success_message = "%(book_name)s was deleted successfully"

	def get_success_url(self):
		return reverse('staff:book_list')

#release book from user
def releasebook(request, id):
	book = get_object_or_404(Book, id=id)
	if request.method == "POST":
		book.status = True
		book.borrower = None
		book.save()
	messages.success(request, 'Book released.')
	return redirect(reverse('staff:book_list'))

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
class DeleteUserView(SuccessMessageMixin, DeleteView):
	model = User
	template_name = "confirm_delete.html"
	pk_url_kwarg = 'id'
	success_message = "%(username)s was deleted successfully"

	def get_success_url(self):
		return reverse('staff:user_list')


#Suggestions
class Suggestions(ListView):
	def get(self, request):
		suggestions = BookSuggestion.objects.all()
		context = {
			'suggestions' : suggestions
		}
		return render(request, 'suggestions.html', context)

class Tagslist(StrongholdPublicMixin, ListView):
	def get(self, request):
		tags = Tags.objects.all()
		context = {
			'tags' : tags,
		}
		return render(request, 'tagslist.html', context)


#Create new tag
class AddTagView(SuccessMessageMixin, CreateView):
	form_class = TagsForm
	model = Tags
	template_name = "staff_add_form.html"
	success_message = "%(name)s was created successfully"

	def get_context_data(self, **kwargs):
		context = super(AddTagView, self).get_context_data(**kwargs)
		context.update({'pagename': "Add new Tag"})
		return context

	def get_success_url(self):
		return reverse('staff:tagslist')

#Update/modify a specific tag
class EditTagView(SuccessMessageMixin, UpdateView):
	form_class = TagsForm
	model = Tags
	template_name = "staff_add_form.html"
	pk_url_kwarg = 'id'
	success_message = "%(name)s was updated successfully"

	def get_context_data(self, **kwargs):
		context = super(EditTagView, self).get_context_data(**kwargs)
		context.update({'pagename': "Update Tag"})
		return context

	def get_success_url(self):
		return reverse('staff:tagslist')


#delete specific tag
class DeleteTagView(SuccessMessageMixin, DeleteView):
	model = Tags
	template_name = "confirm_delete.html"
	pk_url_kwarg = 'id'
	success_message = "item was deleted successfully"

	def get_success_url(self):
		return reverse('staff:tagslist')