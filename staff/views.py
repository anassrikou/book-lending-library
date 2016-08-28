from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse
# Create your views here.
from books.models import Book
from books.forms import BookForm, BookBorrowForm

class BookListView(ListView):
	def get(self, request):
		books = Book.objects.all()
		context = {
			'books' : books,
		}
		return render(request, 'staff_book_list.html', context)


class BookDetailView(DetailView):
	model = Book
	pk_url_kwarg = 'id'
	template_name = "book_detail.html"


class AddBookView(CreateView):
	form_class = BookForm
	model = Book
	template_name = "add_book.html"

	def get_success_url(self):
		return reverse('staff:detail', kwargs={'id' : self.object.id})

class EditBookView(UpdateView):
	form_class = BookForm
	model = Book
	template_name = "add_book.html"
	pk_url_kwarg = 'id'

	def get_success_url(self):
		return reverse('staff:detail', kwargs={'id' : self.object.id})

class DeleteBookView(DeleteView):
	model = Book
	template_name = "confirm_delete.html"
	pk_url_kwarg = 'id'

	def get_success_url(self):
		return reverse('staff:list')
