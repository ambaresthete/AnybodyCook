from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from cart.models import Cart
from .models import Product
from django.core.paginator import Paginator


class ProductFeaturedListView(ListView):
    
    template_name = 'products/list.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured()


class ProductFeaturedDetailView(DetailView):
    
    template_name = 'products/featured_detail.html'
 
    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured()


class ProductListView(ListView):
    template_name = 'products/list.html'

#    def get_context_data(self,*args,**kwargs):
#       context = super(ProductListView,self).get_context_data(*args,**kwargs)
#       print(context)
#       return context

    def get_queryset(self,*args,**kwargs):
        request=self.request
        if request.user.is_authenticated:
            products = Product.objects.exclude(user=request.user)
            paginator = Paginator(products,3)
            page = request.GET.get('page',1)
            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)
            return products
        else:
            products = Product.objects.all()
            paginator = Paginator(products, 3)
            page = request.GET.get('page', 1)
            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)
            return products



class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = 'products/detail.html'

    def get_context_data(self,*args,**kwargs):
        context= super(ProductDetailSlugView,self).get_context_data(*args,**kwargs)
        request=self.request
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Product does not exist")
        except Product.MultipleObjectsReturned:
            qs= Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        return instance

