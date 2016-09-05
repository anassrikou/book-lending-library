from django.shortcuts import render, get_object_or_404,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from .models import Book, Tags, BookBorrow
from .forms import BookForm, BookBorrowForm, SuggestBookForm


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
	form = BookBorrowForm()

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(BookDetailView, self).get_context_data(**kwargs)
		# Add in the publisher
		context['form'] = self.form
		return context

	def post(self, request, id):
		def form_valid(self, form):
			print(form)
			form.save()
		return redirect('/books/')

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


def bookborrow(request, id):
	book_id = get_object_or_404(Book, id=id)
	form = BookBorrowForm(request.POST or None)
	if request.method == "POST":
		if form.is_valid():
			date_borrow_start = form.cleaned_data.get("date_borrow_start")
			date_borrow_end = form.cleaned_data.get("date_borrow_end")
			instance = form.save(commit=False)
			instance.book_borrowed = book_id
			instance.user = User.objects.get(id=request.user.id)
			instance.save()
		return redirect(reverse('books:detail', kwargs={'id': book_id.id}))
	context = {
		'form' : form
	}
	return render(request, 'book_borrow.html', context)

class SuggestBookView(FormView):
	template_name = 'suggestbook.html'
	form_class = SuggestBookForm
	success_url = reverse_lazy('books:list')

	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.
		form.save()
		return super(SuggestBookView, self).form_valid(form)