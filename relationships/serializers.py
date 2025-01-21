# serializers.py
from rest_framework import serializers
from .models import Follower, UserAction
from accounts.serializers import UserPublicSerializer

class FollowerSerializer(serializers.ModelSerializer):
    follower = UserPublicSerializer(read_only=True)
    following = UserPublicSerializer(read_only=True)

    class Meta:
        model = Follower
        fields = ('id', 'follower', 'following', 'created_at')
        read_only_fields = ('follower', 'following', 'created_at')

    def create(self, validated_data):
        # Get user and target from context
        follower = self.context['request'].user
        following = self.context['following_user']

        # Create the follower relationship
        return Follower.objects.create(
            follower=follower,
            following=following
        )

class FollowerListSerializer(serializers.ModelSerializer):
    following = UserPublicSerializer(read_only=True)

    class Meta:
        model = Follower
        fields = ('id', 'following')

class UserActionSerializer(serializers.ModelSerializer):
    target_user = UserPublicSerializer(read_only=True)

    class Meta:
        model = UserAction
        fields = ('id', 'target_user', 'action', 'status', 'created_at', 'updated_at')
        read_only_fields = ('target_user', 'created_at', 'updated_at')

    def validate(self, attrs):
        request = self.context.get('request')
        target_user = self.context.get('target_user')

        # Ensure both users exist
        if not request or not request.user or not target_user:
            raise serializers.ValidationError("Invalid request context")

        # Prevent self-actions
        if request.user == target_user:
            raise serializers.ValidationError("You cannot perform actions on yourself.")

        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['target_user'] = self.context['target_user']
        return super().create(validated_data)