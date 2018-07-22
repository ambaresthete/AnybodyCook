from django.shortcuts import render
from .forms import ProductForm
from products.models import Product

def upload_product(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        if request.user.is_authenticated:
            instance.user = request.user
            instance.save()
    context = {
        "form" : form
    }
    return render(request,"uploads/product_upload.html",context)
