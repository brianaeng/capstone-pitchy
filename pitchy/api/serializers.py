from rest_framework import serializers
from pitchy.models import Focus, Profile, Friendship, Conversation, DirectMessage
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email',]

class FocusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Focus
        fields = ['id', 'name',]

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    focuses = FocusSerializer(read_only=True, many=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'social_handle', 'role', 'focuses',]

class FriendshipSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    friend = UserSerializer()

    class Meta:
        model = Friendship
        fields = ['id', 'user', 'friend', 'confirmed', 'updated_at', 'created_at',]

class ConversationSerializer(serializers.ModelSerializer):
    user1 = UserSerializer()
    user2 = UserSerializer()

    class Meta:
        model = Conversation
        fields = ['id', 'created_at', 'user1', 'user2',]

class DirectMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer
    conversation = ConversationSerializer

    class Meta:
        model = DirectMessage
        fields = ['id', 'sent_at', 'conversation', 'sender', 'body',]
