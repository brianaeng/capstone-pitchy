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

            #Authenticate newly created user
            new_user = authenticate(username=signup_form.cleaned_data['username'], password=signup_form.cleaned_data['password1'],)

            #Log in user after creation
            login(request, new_user)

            #Redirect to profile edit page so they can enter that info
            return redirect('/profile/edit')
        else:
            messages.error(request, ('Please correct the error below.'))
            return render(request, self.template_name, {'signup_form': signup_form})

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profiles/profile.html'
    def get(self, request, pk):
        #Get profile based on pk provided
        profile = get_object_or_404(Profile, pk=pk)

        #Find current user's friends (so we can check if user + profile user are friends)
        current_user_friends = Friendship.objects.filter(Q(user_id=request.user.id) | Q(friend_id=request.user.id))

        #Initialize boolean for friendship (pending or confirmed)
        boolean = False

        #Initialize boolean for confirmed friendship
        confirmed_boolean = False

        #Initialize variable to save friendship
        this_friendship = None

        #Loop through friendships to see if profile user is present
        for friendship in current_user_friends:
            #If profile user is friends with current user, set this_friendship and boolean
            if friendship.user == profile.user or friendship.friend == profile.user:
                this_friendship = friendship

                boolean = True

                #If the friendship is confirmed, set confirmed_boolean
                if this_friendship.confirmed:
                    confirmed_boolean = True

                #Break out if friend is found
                break

        #Build correct URL for chat based on 1) if confirmed friends & 2) if chat already exists
        url = None

        #If friendship exists and is confirmed, see if there's a conversation
        if this_friendship and confirmed_boolean:
            #Query for conversation where current user is user1 & friend is user2 or vice versa
            convo = Conversation.objects.filter(Q(user1=request.user, user2=profile.user) | Q(user1=profile.user, user2=request.user)).first()

            #If there's no convo, set url to True
            if convo == None:
                url = True
            #If there is a convo, set url to the label of it
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
        #Get user and profile form to put both on update profile page
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request):
        #Update user and/or profile on POST request
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/')
        else:
            messages.error(request, ('Please correct the error below.'))
            return render(request, self.template_name, { 'user_form': user_form, 'profile_form': profile_form })

class HomepageView(TemplateView):
    template_name = 'homepage.html'

    def get(self, request):
        #If user is signed in, redirect to the connections page since that's their homepage
        if request.user.is_authenticated():
            return redirect('connections')

        #If they're not redirected, send to generic homepage with welcome info
        return render(request, self.template_name, {})

class ConnectionsView(LoginRequiredMixin, TemplateView):
    template_name = 'connections.html'

    def get(self, request):
        #Pending and comfirmed friendships for current user
        pending_and_confirmed_friends = Friendship.objects.filter(Q(user_id=request.user.id) | Q(friend_id=request.user.id))

        #Profiles of pending/confirmed friends for current user
        profiles = []

        #Harvest friends by looping through friendships (friend can be user or friend so need to grab based on which one the current user isn't)
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
            recommendations = (list(set(users) - set(profiles)))[:5]
        else:
            #If no focuses, give empty recommendations list
            recommendations = []

        return render(request, self.template_name, {'friends': friends, 'friend_requests': friend_requests, 'recommendations': recommendations})

#Allow the user to have a list of potential recipients and a input a message, then send the message to recipient(s)
class CreateChatView(LoginRequiredMixin, FormView):
    template_name = "chat/create_chat.html"

    #Output a form that allows the user to choose the receiver(s) and the message body.
    def get(self, request):
        #Get confirmed friendships
        friendships = Friendship.objects.exclude(confirmed=False).filter(Q(user_id=request.user.id) | Q(friend_id=request.user.id))

        #Get current user's conversations
        conversations = Conversation.objects.filter(Q(user1=request.user) | Q(user2=request.user)).order_by('-updated_at')

        #Profiles of confirmed friends for current user
        users = []

        #Loop through friendships to collect user that's not current user
        for friendship in friendships:
            if friendship.user != request.user:
                users.append(friendship.user)
            else:
                users.append(friendship.friend)

        return render(request, self.template_name, {'users': users, 'conversations': conversations})

    #Create a new chat(s) with message to receiver(s) or add message to pre-established chat with receiver
    def post(self, request):
        #Get message body from request
        message = request.POST['body']

        #Get list of recipient(s) from request
        recipients = request.POST.getlist('recipients')

        #Get current users convos
        current_user_convos = Conversation.objects.filter(Q(user1=request.user) | Q(user2=request.user))

        #For each recipient, find pre-established conversation with them or create new and then add message to that conversation
        for person in recipients:
            #Get person from pk in recipient list
            person_object = User.objects.get(pk=person)

            #If conversation with user exists (either user1 or user2), get conversation
            if current_user_convos.filter(user1=person_object).exists():
                conversation = current_user_convos.get(user1=person_object)
            elif current_user_convos.filter(user2=person_object).exists():
                conversation = current_user_convos.get(user2=person_object)
            #Else, create a new conversation between recipient and current user
            else:
                label = haikunator.haikunate()
                conversation = Conversation.objects.create(user1=request.user, user2=person_object, label=label)

            #Add message to pre-established or new conversation
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

    #Checks to see if current user is part of conversation they are trying to access
    if convo.user1 == request.user or convo.user2 == request.user:
        #Gets conversations for current user sorted by most recently updated (aka by who has most recent message)
        conversations = Conversation.objects.filter(Q(user1=request.user) | Q(user2=request.user)).order_by('-updated_at')

        #Takes last 30 messages, ordered by most recently sent
        messages = reversed(convo.messages.order_by('-sent_at')[:30])

        return render(request, "chat/convo.html", {'convo': convo, 'messages': messages, 'conversations': conversations})
    #If they're not part of the conversation, redirect them to the connections page
    else:
        return redirect("connections")

#Linked in the main nav bar (Messages) w/ the purpose of redirecting to the most recent conversation
def recent_messages(request):
    #Gets conversations for current user sorted by most recently updated (aka by who has most recent message)
    conversations = Conversation.objects.filter(Q(user1=request.user) | Q(user2=request.user)).order_by('-updated_at')

    #If they don't have any conversations, redirect to create conversation page
    if not conversations:
        return redirect('create_chat')
    #Else, redirect them to the most recent conversation
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
    #Find person based on pk argument
    friend = User.objects.get(pk=pk)

    #Find friendship between current user and person
    friendship = Friendship.objects.get(Q(user=request.user, friend=friend) | Q(user=friend, friend=request.user))

    #If users in friendship have a conversation together, delete it
    try:
        conversation = Conversation.objects.get(Q(user1=request.user, user2=friend) | Q(user1=friend, user2=request.user))
        conversation.delete()
    #Else, escape the DoesNotExist error
    except ObjectDoesNotExist:
        pass

    #Delete friendship
    friendship.delete()
    return redirect('connections')

#Display all users for given focus
def focus_users(request, pk):
    #Find the focus from the given pk
    focus = Focus.objects.get(pk=pk)

    #Find the associated users for that focus
    user_set = focus.profile_set.all()

    return render(request, 'profiles/by_focus.html', {'focus': focus, 'user_set': user_set})

#Search bar on the top of the Connections page w/ the purpose of giving search results
def search(request):
    #If search post request is made, take the request text, change to lowercase, and set to search_text
    if request.method == 'POST':
        search_text = request.POST['search_text'].lower()
    #Else set search_text to nothing
    else:
        search_text = ''

    #Query user base by first and last name with search_text (icontains == case insensitive search)
    users = User.objects.filter(Q(first_name__icontains=search_text) | Q(last_name__icontains=search_text))

    return render(request, 'profiles/search.html', {'users': users})
