from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Friendship, Focus, User, Conversation, DirectMessage
from forms import UserForm, ProfileForm, SignUpForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

import random

import string
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
        confirmed_boolean = False
        this_friendship = None
        for friendship in current_user_friends:
            if friendship.user == profile.user or friendship.friend == profile.user:
                this_friendship = friendship

                boolean = True

                if this_friendship.confirmed:
                    confirmed_boolean = True

                break

        #Build correct URL for chat based on 1) if confirmed friends & 2) if chat already exists
        url = None

        if this_friendship and confirmed_boolean:
            convo = Conversation.objects.filter(Q(user1=request.user, user2=profile.user) | Q(user1=profile.user, user2=request.user)).first()

            if convo == None:
                url = True
            else:
                url = convo.label

        #Output role given user's profile
        if profile.role == "PR":
            role = "Public Relations"
        else:
            role = "Journalist"

        return render(request, self.template_name, {'profile': profile, 'role': role, 'boolean': boolean, 'confirmed_boolean': confirmed_boolean, 'url': url})

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

#This is to allow the user to find the person they want to chat, and then pass that to start_chat?
class CreateChatView(LoginRequiredMixin, FormView):
    template_name = "chat/create_chat.html"

    #This should output a form that allows the user to choose the receiver(s) and the message body.
    def get(self, request):
        friendships = Friendship.objects.exclude(confirmed=False).filter(Q(user_id=request.user.id) | Q(friend_id=request.user.id))
        conversations = Conversation.objects.filter(Q(user1=request.user) | Q(user2=request.user)).order_by('-updated_at')


        #Profiles of pending/confirmed friends for current user
        users = []

        for friendship in friendships:
            if friendship.user != request.user:
                users.append(friendship.user)
            else:
                users.append(friendship.friend)

        return render(request, self.template_name, {'users': users, 'conversations': conversations})

    #This should create a new chat(s) with message to receiver(s) or add message to pre-established chat with receiver
    def post(self, request):
        # search_text = request.POST['search_text']
        message = request.POST['body']
        recipients = request.POST.getlist('recipients')
        current_user_convos = Conversation.objects.filter(Q(user1=request.user) | Q(user2=request.user))


        for person in recipients:
            person_object = User.objects.get(pk=person)

            if current_user_convos.filter(user1=person_object).exists():
                conversation = current_user_convos.get(user1=person_object)
            elif current_user_convos.filter(user2=person_object).exists():
                conversation = current_user_convos.get(user2=person_object)
            else:
                label = haikunator.haikunate()
                conversation = Conversation.objects.create(user1=request.user, user2=person_object, label=label)

            conversation.messages.create(sender=request.user.first_name, body=message)

        return redirect(recent_messages)

#This starts a chat with a pre-determined friend via their pk
def start_chat(request, pk):
    friend = User.objects.get(pk=pk)
    label = haikunator.haikunate()
    new_convo = Conversation.objects.create(user1= request.user, user2=friend, label=label)

    return redirect(chat_room, label=label)

#View for a given conversation via the conversation's label
def chat_room(request, label):
    convo = Conversation.objects.get(label=label)

    if convo.user1 == request.user or convo.user2 == request.user:
        conversations = Conversation.objects.filter(Q(user1=request.user) | Q(user2=request.user)).order_by('-updated_at')

        # We want to show the last 50 messages, ordered most-recent-last
        messages = reversed(convo.messages.order_by('-sent_at')[:50])

        return render(request, "chat/convo.html", {'convo': convo, 'messages': messages, 'conversations': conversations})
    else:
        return redirect("connections")

#Linked in the main nav bar (Messages) w/ the purpose of redirecting to the most recent conversation
def recent_messages(request):
    conversations = Conversation.objects.filter(Q(user1=request.user) | Q(user2=request.user)).order_by('-updated_at')

    if not conversations:
        return redirect('create_chat') #Replace this once create conversations page is made
    else:
        last_convo = conversations.first()
        label = last_convo.label
        return redirect(chat_room, label=label)

#Button on the Connections page w/ the purpose of confirming a requested friendship
def confirm_friend(request, pk):
    friendship = Friendship.objects.get(pk=pk)
    friendship.confirmed = True
    friendship.save()
    return redirect('connections')

#Button on the Connections page w/ the purpose of rejecting a requested friendship
def reject_friend(request, pk):
    friendship = Friendship.objects.get(pk=pk)
    friendship.delete()
    return redirect('connections')

#Button on a given Profile page (if not already friends) w/ the purpose of requesting someone to be your friend
def request_friend(request, pk):
    person = User.objects.get(pk=pk)
    Friendship.objects.create(user=request.user, friend=person, confirmed=False)
    return redirect('profile', pk=pk)

#Button on a given Profile page (if friends already) w/ purpose of unfriending the other person
def delete_friend(request, pk):
    friend = User.objects.get(pk=pk)
    friendship = Friendship.objects.get(Q(user=request.user, friend=friend) | Q(friend=friend, user=request.user))

    try:
        conversation = Conversation.objects.get(Q(user1=request.user, user2=friend) | Q(user1=friend, user2=request.user))
        conversation.delete()
    except ObjectDoesNotExist:
        pass

    friendship.delete()
    return redirect('connections')

#Search bar on the top of the Connections page w/ the purpose of giving search results
def search(request):
    if request.method == 'POST':
        search_text = request.POST['search_text'].lower()
    else:
        search_text = ''

    users = User.objects.filter(Q(first_name__icontains=search_text) | Q(last_name__icontains=search_text))

    return render(request, 'profiles/search.html', {'users': users})
