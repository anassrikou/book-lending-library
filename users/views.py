from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from stronghold.decorators import public

from .forms import UserLoginForm, UserRegisterForm

@public
def profile(request, id=None):
    user = get_object_or_404(User, id=id)
    context = {
        'user' : user,
    }
    return render(request, 'profile.html', context)

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
