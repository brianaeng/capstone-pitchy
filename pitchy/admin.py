from django.contrib import admin
from .models import Profile, Focus, Friendship, Conversation, DirectMessage

# Register your models here.
admin.site.register(Profile)
admin.site.register(Focus)
admin.site.register(Friendship)
admin.site.register(Conversation)
admin.site.register(DirectMessage)
