from django import forms

from .models import Book, BookBorrow

class BookForm(forms.ModelForm):
	
	class Meta:
		model = Book
		fields = ["book_name", "author_name", "isbn", "publish_date", "publish_place", "tags", "image", "description", "number_of_pages", "edition"]

class BookBorrowForm(forms.ModelForm):

	class Meta:
		model = BookBorrow
		fields = ["date_borrow_start", "note"]