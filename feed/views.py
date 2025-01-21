from rest_framework import generics, permissions
from posts.serializers import PostSerializer
from posts.views import PostPagination
from django.db.models import Q
from posts.models import Post
from relationships.models import Follower
from relationships.models import UserAction

class FeedView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    pagination_class = PostPagination

    def get_queryset(self):
        user = self.request.user

        # Users I am following
        following_users = Follower.objects.filter(
            follower=user
        ).values_list('following', flat=True)
        
        # Users I have hidden or blocked
        users_i_hidden_blocked = UserAction.objects.filter(
            user=user,
            status=True,
            action__in=[UserAction.ActionChoices.HIDE, UserAction.ActionChoices.BLOCK]
        ).values_list('target_user', flat=True)
        
        # Users who have blocked me
        users_who_blocked_me = UserAction.objects.filter(
            target_user=user,
            status=True,
            action__in= [UserAction.ActionChoices.BLOCK]
        ).values_list('user', flat=True)
        
        # Combine all users to exclude
        excluded_users = set(list(users_i_hidden_blocked) + list(users_who_blocked_me))
        
        # Get posts from followed users, excluding hidden/blocked users
        return Post.objects.filter(
            author__in=following_users
        ).exclude(
            author__in=excluded_users
        ).select_related('author').order_by('-created_at')