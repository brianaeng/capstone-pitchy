from django.http import Http404
from rest_framework import generics
from .serializers import FocusSerializer, ProfileSerializer, UserSerializer, FriendshipSerializer, ConversationSerializer, DirectMessageSerializer
from django.contrib.auth.models import User
from pitchy.models import Focus, Profile, Friendship, User, Conversation, DirectMessage
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

#FILTERS:
# class ProfileFilter(django_filters.rest_framework.FilterSet):
#     min_price = django_filters.NumberFilter(name="price", lookup_expr='gte')
#     max_price = django_filters.NumberFilter(name="price", lookup_expr='lte')
#     class Meta:
#         model = Profile
#         fields = ['category', 'in_stock', 'min_price', 'max_price']

#GET REQUESTS:

#QUERY PROFILES
class UserSearchAPIView(generics.ListAPIView):
   queryset = Profile.objects.all()
   serializer_class = ProfileSerializer
   filter_backends = [SearchFilter]
   search_fields = ['user__first_name', 'user__last_name']
   #example search: http://127.0.0.1:8000/api/pitchy/?search=bri%20test

#GET ALL FOCUSES @ api/pitchy/focuses/
class FocusListAPIView(generics.ListAPIView):
    serializer_class = FocusSerializer

    def get_queryset(self):
        return Focus.objects.all()

#GET ALL PROFILES @ api/pitchy/users
class ProfileListAPIView(generics.ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.all()

#GET FRIENDS LIST FOR CURRENT USER @ api/pitchy/friendships
class FriendshipListAPIView(generics.ListAPIView):
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.exclude(confirmed=False).filter(Q(user_id=user.id) | Q(friend_id=user.id))

#GET FRIEND REQUESTS LIST FOR CURRENT USER @ api/pitchy/friendshiprequests
class FriendRequestListAPIView(generics.ListAPIView):
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.all().filter(friend_id=user.id, confirmed=False)

#GET CONVERSATIONS FOR CURRENT USER @ api/pitchy/conversations
class ConversationListAPIView(generics.ListAPIView):
    serializer_class = ConversationSerializer

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(Q(user1=user) | Q(user2=user))

#GET MESSAGES FOR CURRENT USER'S SPECIFIC CONVERSATION @ api/pitchy/conversations/ID/messages
class DirectMessageListAPIView(generics.ListAPIView):
    serializer_class = DirectMessageSerializer

    def get_queryset(self):
        user = self.request.user
        pk = self.kwargs['pk']
        selected_convo = Conversation.objects.get(pk=pk)

        if (selected_convo.user1 == user or selected_convo.user2 == user):
            selected_convo = Conversation.objects.get(pk=pk)
            return DirectMessage.objects.filter(conversation_id=selected_convo.id)
        else:
            return []
#CREATE REQUESTS:

#CREATE A USER
class CreateUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#CREATE A PROFILE
class CreateProfileAPIView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

#CREATE A CONVERSATION
class CreateConversationAPIView(generics.CreateAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

#CREATE A MESSAGE
class CreateDirectMessageAPIView(generics.CreateAPIView):
    queryset = DirectMessage.objects.all()
    serializer_class = DirectMessageSerializer

#VIEWSETS

#GET/PUT/PATCH A USER
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

# Don't need these?
# class UserListAPIView(generics.ListAPIView):
#     serializer_class = UserSerializer
#
#     def get_queryset(self):
#         return User.objects.all()

#GET ONE USER @ api/pitchy/users/ID
# class UserDetailAPIView(generics.RetrieveAPIView):
#     serializer_class = ProfileSerializer
#
#     def get_queryset(self):
#         pk = self.kwargs['pk']
#         return Profile.objects.filter(pk=pk)
