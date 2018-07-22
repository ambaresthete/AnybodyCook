from django.conf.urls import url

from .views import assign_role

urlpatterns = [
    url(r'^$', assign_role, name='role'),
    
]
