from django.contrib import admin
from .models import Profile, Focus, Friendship

# Register your models here.
admin.site.register(Profile)
admin.site.register(Focus)
admin.site.register(Friendship)
