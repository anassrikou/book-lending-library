from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from stronghold.decorators import public
from django.views.generic.edit import  UpdateView
from django.core.urlresolvers import reverse

from .forms import UserLoginForm, UserRegisterForm, VisitorForm, UpdateForm


@public
def profile(request, id=None):
    return render(request, 'profile.html')


def update(request, id=None):
    form = UpdateForm(request.POST or None, instance = request.user)
    form2 = VisitorForm(request.POST or None, instance = request.user.visitor)
    if form.is_valid() and form2.is_valid():
        cin = form2.cleaned_data.get('cin')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        user = form.save(commit=False)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return redirect(user.visitor.get_absolute_url())
    context = {
        "form" : form,
        "form2" : form2,
        "title" : "Update Profile"
    }
    return render(request, 'form.html', context)

def login_view(request):
    next = request.GET.get('next')
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect(reverse('index'))
    return render(request, "form.html", {"form":form, "title": title})

@public
def register_view(request):
    next = request.GET.get('next')
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    form2 = VisitorForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect(reverse('index'))

    context = {
        "form": form,
        "title": title
    }
    return render(request, "form.html", context)


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))
