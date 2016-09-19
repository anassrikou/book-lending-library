from django.contrib import admin
from .models import Book, Tags, BookBorrow, BookSuggestion
# Register your models here.

class BookAdmin(admin.ModelAdmin):
	list_display = ["book_name", "created", "borrower", "status"]

	class Meta:
		model = Book

class BookBorrowAdmin(admin.ModelAdmin):
	list_display = ["date_borrow_start", "book_borrowed", "user"]

	class Meta:
		model = BookBorrow

class SuggestionAdmin(admin.ModelAdmin):
	list_display = ["book_name", "created"]

admin.site.register(Book, BookAdmin)
admin.site.register(Tags)
admin.site.register(BookBorrow, BookBorrowAdmin)
admin.site.register(BookSuggestion, SuggestionAdmin)