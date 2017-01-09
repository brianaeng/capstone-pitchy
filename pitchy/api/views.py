from rest_framework import generics
from .serializers import FocusSerializer, ProfileSerializer, UserSerializer, FriendshipSerializer, ConversationSerializer, DirectMessageSerializer
from pitchy.models import Focus, Profile, Friendship, User, Conversation, DirectMessage
from django.db.models import Q
from rest_framework import viewsets


class ProfileViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    #Look into these?
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                           IsOwnerOrReadOnly,)

    # def get_queryset(self):
    #     return Profile.objects.filter(pk=pk)

class FocusListAPIView(generics.ListAPIView):
    serializer_class = FocusSerializer

    def get_queryset(self):
        return Focus.objects.all()

class ProfileListAPIView(generics.ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.all()

class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

# class UserDetailAPIView(generics.RetrieveAPIView):
#     serializer_class = ProfileSerializer
#
#     def get_queryset(self):
#         pk = self.kwargs['pk']
#         return Profile.objects.filter(pk=pk)

class FriendshipListAPIView(generics.ListAPIView):
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.exclude(confirmed=False).filter(Q(user_id=user.id) | Q(friend_id=user.id))

class FriendRequestListAPIView(generics.ListAPIView):
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.all().filter(friend_id=user.id, confirmed=False)

class ConversationListAPIView(generics.ListAPIView):
    serializer_class = ConversationSerializer

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(Q(user1=user) | Q(user2=user))

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
