from django.conf.urls import url

from .views import upro

urlpatterns = [
    url(r'^$', upro , name='upro'),
    
]
