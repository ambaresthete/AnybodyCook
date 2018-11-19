from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
User = settings.AUTH_USER_MODEL


class Upro(models.Model):
    user = models.ForeignKey(User)
    desc = models.CharField(max_length=128)
    special = models.CharField(max_length=128)
    image = models.ImageField(upload_to="uimages/")


    def __str__(self):
        return self.user.username
