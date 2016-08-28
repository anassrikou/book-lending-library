from django import forms

from .models import Book, BookBorrow

class BookForm(forms.ModelForm):
	
	class Meta:
		model = Book
		fields = ["book_name", "author_name", "isbn", "publish_date", "publish_place", "tags", "image", "description", "number_of_pages", "edition"]

class BookBorrowForm(forms.ModelForm):
	date_borrow_start = forms.DateField(widget=forms.SelectDateWidget())
	date_borrow_end = forms.DateField(widget=forms.SelectDateWidget())

	def clean(self, *args, **kwargs):
		date_borrow_start = self.cleaned_data.get("date_borrow_start")
		date_borrow_end = self.cleaned_data.get("date_borrow_end")

		if date_borrow_end < date_borrow_start:
			raise forms.ValidationError("return date cant be before borrow date")


	class Meta:
		model = BookBorrow
		fields = ["date_borrow_start", "date_borrow_end", "note",]