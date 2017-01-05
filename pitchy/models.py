from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Focus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    social_handle = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=50, blank=True)
    focuses = models.ManyToManyField(Focus)
    is_pr = models.BooleanField(default=False)
    is_journo = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Friendship(models.Model):
    user = models.ForeignKey(User, related_name="friendship_requestor")
    friend = models.ForeignKey(User, related_name="friendship_requestee")
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        output = "{} requested {} - confirmation: {}".format(self.user, self.friend, self.confirmed)
        return output
