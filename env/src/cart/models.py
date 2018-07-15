from django.conf import settings
from django.db import models
from products.models import Product
from django.db.models.signals import pre_save, m2m_changed

# Create your models here.
User= settings.AUTH_USER_MODEL

class CartManager(models.Manager):
    def new_or_get(self,request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj=False
            cart_obj = qs.first()
            if request.user.is_authenticated() and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj=True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj    
    def new(self,user=None):
        user_obj=None
        if user is not None:
            if user.is_authenticated():
                user_obj=user
        return self.model.objects.create(user=user_obj)    
        

class Cart(models.Model):
    user       = models.ForeignKey(User,null=True,blank=True)
    products   = models.ManyToManyField(Product,blank=True)
    timestamp  = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True)
    subtotal   = models.DecimalField(default=0.00,max_digits=100,decimal_places=2)
    total      = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

    objects=CartManager()

    def __str__(self):
        return str(self.id)

def m2m_changed_cart_receiver(sender, instance,action,*args,**kwargs):
    print(action)
    print(instance.subtotal)
    if action == "post_add" or action == "post_remove" or action == "post_clear":
        products = instance.products.all()
        subtotal=0
        for i in products:
            subtotal += i.price
        instance.subtotal = subtotal
        instance.save()          


m2m_changed.connect(m2m_changed_cart_receiver,sender=Cart.products.through)

def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    instance.total=instance.subtotal


pre_save.connect(pre_save_cart_receiver,sender=Cart)
