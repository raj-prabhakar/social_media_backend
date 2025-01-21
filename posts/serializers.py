from rest_framework import serializers
from .models import Post
from accounts.serializers import UserPublicSerializer

class PostSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'content', 'author', 'created_at', 'updated_at', 'is_author')
        read_only_fields = ('author', 'created_at', 'updated_at')

    def get_is_author(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.author == request.user
        return False

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)