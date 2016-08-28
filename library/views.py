from django.shortcuts import render

def homepage(request):
	return render(request, 'index.html')

def contactus(request):
	return render(request, 'contact.html')