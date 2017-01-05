from django.shortcuts import render, redirect
from .models import Profile, Friendship, Focus
from forms import UserForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView
from django.db.models import Q

class UpdateProfileView(LoginRequiredMixin, FormView):
    template_name = 'profiles/update_profile.html'

    def get(self, request):
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('/')
        else:
            messages.error(request, ('Please correct the error below.'))

class HomepageView(TemplateView):
    template_name = 'homepage.html'

    def get(self, request):
        return render(request, self.template_name, {})

class HubView(LoginRequiredMixin, TemplateView):
    template_name = 'hub.html'

    def get(self, request):
        friends = Friendship.objects.exclude(confirmed=False).filter(Q(user_id=request.user.id) | Q(friend_id=request.user.id))
        friend_requests = Friendship.objects.all().filter(friend_id=request.user.id, confirmed=False)
        return render(request, self.template_name, {'friends': friends, 'friend_requests': friend_requests })
