from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Book, Tags, BookBorrow
from .forms import BookForm, BookBorrowForm

# # Create your views here.
# def book_list(request):
# 	books = Book.objects.all()
# 	tags = Tags.objects.all()
# 	query = request.GET.get("q")
# 	if query:
# 		books = books.filter(
# 				Q(book_name__icontains=query)|
# 				Q(author_name__icontains=query)|
# 				Q(tags__name__icontains=query)
# 				).distinct()
# 	context = {
# 		'books' : books,
# 		'tags' : tags
# 	}
# 	return render(request, 'book_list.html', context)

# def book_detail(request, id=None):
# 	book = get_object_or_404(Book, id=id)
# 	tags = Tags.objects.all()
# 	context = {
# 		'book' : book,
# 		'tags' : tags
# 	}
# 	return render(request, 'book_detail.html', context)


class BookListView(ListView):
	def get(self, request):
		books = Book.objects.all()
		tags = Tags.objects.all()
		query = request.GET.get("q")
		if query:
			books = books.filter(
			Q(book_name__icontains=query)|
			Q(author_name__icontains=query)|
			Q(tags__name__icontains=query)
			).distinct()

		paginator = Paginator(books, 3) # Show 25 contacts per page

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
			'tags' : tags
			}
		return render(request, 'book_list.html', context)


class BookDetailView(DetailView):
	model = Book
	pk_url_kwarg = 'id'
	template_name = "book_detail.html"
	
	def post(self, request):
		pass

class AddBookView(CreateView):
	form_class = BookForm
	model = Book
	template_name = "add_book.html"

	def get_success_url(self):
		return reverse('books:detail', kwargs={'id' : self.object.id})

class EditBookView(UpdateView):
	form_class = BookForm
	model = Book
	template_name = "add_book.html"
	pk_url_kwarg = 'id'

	def get_success_url(self):
		return reverse('books:detail', kwargs={'id' : self.object.id})

class DeleteBookView(DeleteView):
	model = Book
	template_name = "confirm_delete.html"
	pk_url_kwarg = 'id'

	def get_success_url(self):
		return reverse('books:list')


class BorrowBookView(CreateView):
	model = BookBorrow
	template_name = "book_borrow.html"
	pk_url_kwarg = 'id'

	def get_success_url(self):
		return reverse('books:detail', kwargs={'id': self.object.id})