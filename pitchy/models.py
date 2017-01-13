from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

# Create your models here.
class Focus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pic = models.ImageField(blank=True)
    bio = models.TextField()
    social_handle = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=50, blank=True)
    focuses = models.ManyToManyField(Focus)
    role = models.CharField(max_length=30, choices=(("PR", "Public Relations Professional"), ("JOURNO", "Journalist")))

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

class Conversation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    label = models.UUIDField(default=uuid.uuid4, editable=False)
    user1 = models.ForeignKey(User, related_name="user_one")
    user2 = models.ForeignKey(User, related_name="user_two")

    def __str__(self):
        output = "{} & {} convo".format(self.user1, self.user2)
        return output

class DirectMessage(models.Model):
    #add a read_at?
    sent_at = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, related_name="messages")
    # sender = models.ForeignKey(User, related_name="message_sender")
    sender = models.TextField()
    body = models.TextField()
    # attachment = models.FileField(blank=True, )

    def __str__(self):
        output = "{}: {}".format(self.sender, self.body)
        return output
