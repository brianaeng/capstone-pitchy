from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Friendship, Focus, User, Conversation, DirectMessage
from forms import UserForm, ProfileForm, SignUpForm
from django.contrib import messages
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

class SignUpView(FormView):
    template_name = 'registration/signup.html'

    def get(self, request):
        signup_form = SignUpForm()
        return render(request, self.template_name, {'signup_form': signup_form})

    def post(self, request):
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            messages.success(request, ('Your account was successfully created!'))
            new_user = authenticate(username=signup_form.cleaned_data['username'], password=signup_form.cleaned_data['password1'],)
            login(request, new_user)
            return redirect('/profile/edit')
        else:
            messages.error(request, ('Please correct the error below.'))
            return render(request, self.template_name, {'signup_form': signup_form})

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profiles/profile.html'
    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        current_user_friends = Friendship.objects.filter(Q(user_id=request.user.id) | Q(friend_id=request.user.id))
        boolean = False
        for friendship in current_user_friends:
            if friendship.user == profile.user or friendship.friend == profile.user:
                boolean = True
                break

        if profile.role == "PR":
            role = "Public Relations"
        else:
            role = "Journalist"

        return render(request, self.template_name, {'profile': profile, 'role': role, 'boolean': boolean})

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
            return render(request, self.template_name, {
                'user_form': user_form,
                'profile_form': profile_form
            })

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

class ConversationView(LoginRequiredMixin, TemplateView):
    template_name = 'messaging/conversations.html'

    def get(self, request, pk):
        conversations = Conversation.objects.filter(Q(user1=request.user) | Q(user2=request.user))
        selected_convo = Conversation.objects.get(pk=pk)
        messages = DirectMessage.objects.filter(conversation_id=selected_convo.id)
        return render(request, self.template_name, {'conversations': conversations, 'messages': messages})

def confirm_friend(request, pk):
    friendship = Friendship.objects.get(pk=pk)
    friendship.confirmed = True
    friendship.save()
    return redirect('hub')

def request_friend(request, pk):
    person = User.objects.get(pk=pk)
    Friendship.objects.create(user=request.user, friend=person, confirmed=False)
    return redirect('profile', pk=pk)
