from django.conf.urls import url

from .views import upload_product

urlpatterns = [
    url(r'^$', upload_product, name='product'),

]
