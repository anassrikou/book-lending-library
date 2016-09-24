from django.shortcuts import render
from stronghold.decorators import public
from books.models import Book


@public
def homepage(request):	
	return render(request, 'index.html')


@public
def contactus(request):
	return render(request, 'contact.html')