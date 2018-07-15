
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContactForm

def home_page(request):
    context={
        "title":"Home Page",
        "content":"Under Construction"
    }
   # return render(request,"home_page.html",context)
    return redirect("products/")

def about_page(request):
    context = {
        "title": "About Page",
        "content": "Welcome to about page"
    }
    return render(request, "home_page.html", context)


def contact_page(request):
    form=ContactForm(request.POST or None)
    context = {
        "title": "Contact Page",
        "content": "Welcome to contact page",
        "form": form
    }
    if form.is_valid():
        print(form.cleaned_data)
    return render(request, "contact/view.html", context)

