from django import forms
from django.contrib.auth.models import User
from .models import Profile, Focus
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'social_handle', 'company', 'focuses')

class FocusForm(forms.ModelForm):
    class Meta:
        model = Focus
        fields = ('name',)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
