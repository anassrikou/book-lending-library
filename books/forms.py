from django import forms

from .models import Book, BookBorrow, BookSuggestion, Tags

class BookForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ["book_name", "author_name", "isbn", "publish_date", "publish_place", "tags", 
				 "description", "number_of_pages", "edition"]


class BookBorrowForm(forms.ModelForm):
	date_borrow_start = forms.DateField(widget=forms.DateInput(attrs={'id': 'datepicker', 'placeholder': 'ex: 2016-02-22'}))
	date_borrow_end = forms.DateField(widget=forms.DateInput(attrs={'id': 'datepicker', 'placeholder': 'ex: 2016-02-29'}))

	# def clean(self, *args, **kwargs):
		# date_borrow_start = self.cleaned_data.get("date_borrow_start")
		# date_borrow_end = self.cleaned_data.get("date_borrow_end")

		# if date_borrow_end < date_borrow_start:
		# 	raise forms.ValidationError("return date cant be before borrow date")

	class Meta:
		model = BookBorrow
		fields = ["date_borrow_start", "date_borrow_end", "note",]


class SuggestBookForm(forms.ModelForm):
	class Meta:
		model = BookSuggestion
		fields = ["book_name", "isbn", "author_name", "comment"]


class TagsForm(forms.ModelForm):
	class Meta:
		model = Tags
		fields = ["name"]