from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Post
from .serializers import PostSerializer
from relationships.models import UserAction  
class PostPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a post to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of the post.
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    pagination_class = PostPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.all()
        
        username = self.request.query_params.get('author', None)
        if username:
            # Remove any quotes from the username
            username = username.strip('"')
            queryset = queryset.filter(author__username=username)
        
        # Exclude posts from blocked and hidden users
        if self.request.user.is_authenticated:
            blocked_hidden = UserAction.objects.filter(
                user=self.request.user,
                action__in=['HIDE', 'BLOCK'],
                status=True
            ).values_list('target_user', flat=True)
            queryset = queryset.exclude(author__in=blocked_hidden)
        
        # return queryset    
        return queryset.select_related('author')

    def perform_create(self, serializer):
        """Set the author to the current user when creating a post"""
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)