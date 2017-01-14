from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Friendship, Focus, User, Conversation, DirectMessage
from forms import UserForm, ProfileForm, SignUpForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
import random
from django.core.exceptions import ObjectDoesNotExist

import string
from django.db import transaction
import haikunator

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

        #See if profile user is friends with current user
        current_user_friends = Friendship.objects.filter(Q(user_id=request.user.id) | Q(friend_id=request.user.id))
        boolean = False
        this_friendship = None
        for friendship in current_user_friends:
            if friendship.user == profile.user or friendship.friend == profile.user:
                this_friendship = friendship
                boolean = True
                break

        if profile == request.user.profile:
            boolean = True

        #Build correct URL for chat based on 1) if confirmed friends & 2) if chat already exists
        url = None

        if this_friendship and this_friendship.confirmed:
            convo = Conversation.objects.filter(Q(user1=request.user, user2=profile.user) | Q(user1=profile.user, user2=request.user)).first()

            #This is inefficient in the longrun bc it creates a conversation for EVERY friendship if the profile page is accessed a friend, instead of the user actively making the conversation
            if convo == None:
                label = haikunator.haikunate()
                new_convo = Conversation.objects.create(user1=request.user, user2=profile.user, label=label)

                url = new_convo.label
            else:
                url = convo.label

        #Output role given user's profile
        if profile.role == "PR":
            role = "Public Relations"
        else:
            role = "Journalist"

        return render(request, self.template_name, {'profile': profile, 'role': role, 'boolean': boolean, 'url': url})

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
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
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
        if request.user.is_authenticated():
            return redirect('connections')
        return render(request, self.template_name, {})

class ConnectionsView(LoginRequiredMixin, TemplateView):
    template_name = 'connections.html'

    def get(self, request):
        #Pending and comfirmed friendships for current user
        pending_and_confirmed_friends = Friendship.objects.filter(Q(user_id=request.user.id) | Q(friend_id=request.user.id))

        #Profiles of pending/confirmed friends for current user
        profiles = []

        for friendship in pending_and_confirmed_friends:
            if friendship.user != request.user:
                profiles.append(friendship.user.profile)
            else:
                profiles.append(friendship.friend.profile)

        #Confirmed friends for current user
        friends = pending_and_confirmed_friends.exclude(confirmed=False)

        #Pending friend requests for current user
        friend_requests = Friendship.objects.filter(friend_id=request.user.id, confirmed=False)

        #Current user profile
        user_profile = Profile.objects.get(user_id=request.user.id)

        if user_profile.focuses.all():
            #All of current user's focuses
            user_focuses = user_profile.focuses.all()

            #Randomly choose a focus
            focus = random.choice(user_focuses)

            #Users with chosen focus (excluding current user)
            users = focus.profile_set.all().exclude(id=user_profile.id)

            #Cross reference focus users with current user's friends
            recommendations = list(set(users) - set(profiles))
        else:
            recommendations = []

        return render(request, self.template_name, {'friends': friends, 'friend_requests': friend_requests, 'recommendations': recommendations})

class ConversationView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/conversations.html'

    def get(self, request):
        conversations = Conversation.objects.filter(Q(user1=request.user) | Q(user2=request.user))
        # selected_convo = Conversation.objects.get(pk=pk)
        # messages = DirectMessage.objects.filter(conversation_id=selected_convo.id)
        return render(request, self.template_name, {'conversations': conversations})

def confirm_friend(request, pk):
    friendship = Friendship.objects.get(pk=pk)
    friendship.confirmed = True
    friendship.save()
    return redirect('connections')

def request_friend(request, pk):
    person = User.objects.get(pk=pk)
    Friendship.objects.create(user=request.user, friend=person, confirmed=False)
    return redirect('profile', pk=pk)

def search(request):
    if request.method == 'POST':
        search_text = request.POST['search_text'].lower()
    else:
        search_text = ''

    users = User.objects.filter(Q(first_name__icontains=search_text) | Q(last_name__icontains=search_text))

    return render(request, 'profiles/search.html', {'users': users})

def new_chat(request):
    """
    Randomly create a new room, and redirect to it.
    """
    label = haikunator.haikunate()
    new_convo = Conversation.objects.create(user1= request.user, user2=request.user, label=label)

    return redirect(chat_room, label=label)

def chat_room(request, label):
    """
    Room view - show the room, with latest messages.

    The template for this view has the WebSocket business to send and stream
    messages, so see the template for where the magic happens.
    """
    # If the room with the given label doesn't exist, automatically create it
    # upon first visit (a la etherpad).
    room, created = Conversation.objects.get_or_create(label=label)

    # We want to show the last 50 messages, ordered most-recent-last
    messages = reversed(room.messages.order_by('-sent_at')[:50])

    return render(request, "chat/room.html", {
        'room': room,
        'messages': messages,
    })
