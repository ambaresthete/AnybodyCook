"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.conf.urls import url, include
from django.contrib import admin
from addresses.views import checkout_address_create_view
from accounts.views import login_page, register_page, logout_page
from .views import  home_page, about_page, contact_page

urlpatterns = [
    url(r'^$', home_page, name='home'),
    url(r'^about/$', about_page, name='about'),
    url(r'^contact/$', contact_page, name='contact'),
    url(r'^checkout/address/create/$', checkout_address_create_view, name='checkout_address_create'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', login_page, name='login'),
    url(r'^logout/$',logout_page,name='logout'),
    url(r'^register/$', register_page, name='register'),
    url(r'^products/', include('products.urls', namespace='products')),
    url(r'^search/', include('search.urls', namespace='search')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^upload/', include('upload.urls', namespace='upload')),
    url(r'^roles/', include('roles.urls', namespace='roles')),
    url(r'^pro/', include('uprofile.urls', namespace='pro')),


]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
