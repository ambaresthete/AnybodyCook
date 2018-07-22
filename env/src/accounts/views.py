from django.contrib.auth import authenticate, login, get_user_model, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.utils.http import is_safe_url
from roles.models import Role

def login_page(request):
    form = LoginForm(request.POST or None)
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_url = next_ or next_post or None
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            role = Role.objects.get(user=user)
            request.session['rolename'] = role.rolename
            if is_safe_url(redirect_url, request.get_host()):
                return redirect(redirect_url)
            else:
                return redirect("/")    
        else:
            print("Error")
    context = {
        "form": form
    }
    return render(request, "accounts/login.html", context)


User = get_user_model()


def register_page(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = User.objects.create_user(username, email, password)
        return redirect('login')
    context = {
        "form": form
    }
    return render(request, "accounts/register.html", context)

def logout_page(request):
    logout(request)
    return redirect('/login')
