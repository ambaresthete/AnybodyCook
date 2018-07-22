from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
User = settings.AUTH_USER_MODEL

ROLE_CHOICES = (("user","User"),
("cook","Cook")
)

class Role(models.Model):
    user = models.ForeignKey(User)
    rolename = models.CharField(max_length=120, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username


def post_save_receiver(sender, instance, created, *args, **kwargs):
    if created:
        role = "user"
        Role.objects.create(user=instance, rolename=role)


post_save.connect(post_save_receiver, sender=User)
