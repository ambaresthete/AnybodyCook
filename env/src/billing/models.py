from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL



class BillingProfile(models.Model):
    user = models.OneToOneField(User,null=True, blank=True)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

def user_created_receiver(sender, instance ,created,*args,**kwargs):
    if created:
        BillingProfile.objects.get_or_create(user=instance)


post_save.connect(user_created_receiver, sender= User)
