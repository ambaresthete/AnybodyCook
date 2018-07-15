import random
import os
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from ecommerce.utils import unique_slug_generator
from django.urls import reverse


def get_name_ext(filepath):
    basename = os.path.basename(filepath)
    name, ext= os.path.splitext(basename)
   # print(basename)
    return name, ext

def upload_image_to(instance, filename):
   # print(instance)
   # print(filename)
    new_filename = random.randint(1,4325783789)
    name, ext = get_name_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )
class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True,active=True)

    def search(self,query):
        lookups = Q(title__icontains=query) | Q(description__icontains=query)
        return self.filter(lookups).distinct()    

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()    

    def featured(self):
        return self.get_queryset().featured()   

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self,query):
        return self.get_queryset().search(query)    

class Product(models.Model):
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price       = models.DecimalField(decimal_places=2,max_digits=20)
    image       = models.ImageField(upload_to=upload_image_to, null=True, blank=True)
    featured    = models.BooleanField(default=False) 
    active      = models.BooleanField(default=True)
    timestamp   = models.DateTimeField(auto_now_add=True)


    objects = ProductManager()

    def get_absolute_url(self):
        return reverse("products:detail",kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

def product_pre_save_receiver(sender, instance , *args, **kwargs):
    print(sender)
    print(instance)
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)        

pre_save.connect(product_pre_save_receiver, sender = Product)
