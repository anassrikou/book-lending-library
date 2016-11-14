from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from stronghold.views import StrongholdPublicMixin

from books.forms import BookBorrowForm, BookForm, TagsForm
from books.models import Book, BookSuggestion, Tags


class HomePageView(TemplateView):
	def get(self, request, *args, **kwargs):
		if not request.user.is_staff:
			return render(request, 'no_access.html')
		else:
			return render(request, 'staff_homepage.html')


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
		if not request.user.is_staff:
			return render(request, 'no_access.html')
		else:
			return render(request, 'staff_book_list.html', context)


class AddBookView(SuccessMessageMixin, CreateView):
	
	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_staff:
			return render(request, 'no_access.html')
		return super(AddBookView, self).dispatch(request, *args, **kwargs)

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


class EditBookView(SuccessMessageMixin, UpdateView):

	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_staff:
			return render(request, 'no_access.html')
		return super(EditBookView, self).dispatch(request, *args, **kwargs)

	form_class = BookForm
	model = Book
	pk_url_kwarg = 'id'
	template_name = "staff_add_form.html"
	success_message = "%(book_name)s was updated successfully"

	def get_context_data(self, **kwargs):
		context = super(EditBookView, self).get_context_data(**kwargs)
		context.update({'pagename': "Update Book"})
		return context

	def get_success_url(self):
		return reverse('staff:book_list')


class DeleteBookView(SuccessMessageMixin, View):
	
	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_staff:
			return render(request, 'no_access.html')
		return super(DeleteBookView, self).dispatch(request, *args, **kwargs)
		
	def delete(self, request, id):
    # delete an object and send a confirmation response
	    Book.objects.get(pk = id).delete()
	    return HttpResponse('deleted!')


# def deleteBook(request, id):
# 	if request.method == "DELETE":
# 		Book.objects.get(pk=request.DELETE['pk']).delete()
# 		return HttpResponse('deleted!', content_type="text/plain")
# 	return HttpResponse('not working!')


"""
delete user from the book isntance and change its status
args = id of the user
return = redirect
"""
def releasebook(request, id):
	if not request.user.is_staff:
			return render(request, 'no_access.html')
	else:
		book = get_object_or_404(Book, id=id)
		if request.method == "POST":
			book.status = True
			book.borrower = None
			book.save()
		messages.success(request, 'Book released.')
		return redirect(reverse('staff:book_list'))


"""
args = None
return = list of all the users including the staff
"""
class UserListView(ListView):
	def get(self, request):
		users = User.objects.all()
		context = {
			'users' : users
		}
		if not request.user.is_staff:
			return render(request, 'no_access.html')
		else:
			return render(request, 'staff_user_list.html', context)


"""
delete a specific user from the database
args = id of the user
return = refresh
"""
class DeleteUserView(SuccessMessageMixin, View):
	
	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_staff:
			return render(request, 'no_access.html')
		return super(DeleteUserView, self).dispatch(request, *args, **kwargs)
		
	def delete(self, request, id):
    # delete an object and send a confirmation response
	    user = User.objects.get(pk = id)
	    if not user.is_staff:
	    	user.delete()
	    return HttpResponse('deleted!')

"""
list all the suggestions from the database 
args = None
return = list
"""
class Suggestions(ListView):
	def get(self, request):
		suggestions = BookSuggestion.objects.all()
		context = {
			'suggestions' : suggestions
		}
		if not request.user.is_staff:
			return render(request, 'no_access.html')
		else:
			return render(request, 'suggestions.html', context)


"""
return list of the tags from the database 
args = None
return = list
"""
class Tagslist(StrongholdPublicMixin, ListView):
	def get(self, request):
		tags = Tags.objects.all()
		context = {
			'tags' : tags,
		}
		if not request.user.is_staff:
			return render(request, 'no_access.html')
		else:
			return render(request, 'staff_tags_list.html', context)


"""
create a new tag and store in the database
args = data from the form
return = redirect
"""
class AddTagView(SuccessMessageMixin, CreateView):
	
	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_staff:
			return render(request, 'no_access.html')
		return super(AddTagView, self).dispatch(request, *args, **kwargs)
	
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


"""
modify a specific tag
args = id
return = redirect
"""
class EditTagView(SuccessMessageMixin, UpdateView):
	
	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_staff:
			return render(request, 'no_access.html')
		return super(EditTagView, self).dispatch(request, *args, **kwargs)
	
	form_class = TagsForm
	model = Tags
	pk_url_kwarg = 'id'
	template_name = "staff_add_form.html"
	success_message = "%(name)s was updated successfully"

	def get_context_data(self, **kwargs):
		context = super(EditTagView, self).get_context_data(**kwargs)
		context.update({'pagename': "Update Tag"})
		return context

	def get_success_url(self):
		return reverse('staff:tagslist')


"""
delete a specific tag
args = id
return = redirect
"""
class DeleteTagView(SuccessMessageMixin, DeleteView):
	
	def delete(self, request, id):
    # delete an object and send a confirmation response
	    Tags.objects.get(pk = id).delete()
	    return HttpResponse('deleted!')
	# model = Tags
	# pk_url_kwarg = 'id'
	# template_name = "confirm_delete.html"
	# success_message = "item was deleted successfully"

	# def get_success_url(self):
	# 	return reverse('staff:tagslist')
