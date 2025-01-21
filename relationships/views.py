# views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Follower, UserAction
from .serializers import FollowerSerializer, FollowerListSerializer, UserActionSerializer
from accounts.models import CustomUser

class FollowView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowerSerializer

    @transaction.atomic
    def post(self, request, username):
        target_user = get_object_or_404(CustomUser, username=username)
        
        # Check if user is trying to follow themselves
        if request.user == target_user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if user already follows the target user
        if Follower.objects.filter(
            follower=request.user,
            following=target_user
        ).exists():
            return Response(
                {"detail": "You are already following this user."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check for blocks
        if UserAction.objects.filter(
            user=target_user,
            target_user=request.user,
            action=UserAction.ActionChoices.BLOCK,
            status=True
        ).exists() or UserAction.objects.filter(
            user=request.user,
            target_user=target_user,
            action=UserAction.ActionChoices.BLOCK,
            status=True
        ).exists():
            return Response(
                {"detail": "Unable to follow this user."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Create follow relationship
        serializer = self.get_serializer(
            data={},
            context={'request': request, 'following_user': target_user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UnfollowView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        # Check if trying to unfollow self
        if username == request.user.username:
            return Response(
                {"detail": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        target_user = get_object_or_404(CustomUser, username=username)
        
        # Check if currently following
        follow_relationship = Follower.objects.filter(
            follower=request.user,
            following=target_user
        )
        
        if not follow_relationship.exists():
            return Response(
                {"detail": "You are not following this user."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check for blocks
        if UserAction.objects.filter(
            user=target_user,
            target_user=request.user,
            action=UserAction.ActionChoices.BLOCK,
            status=True
        ).exists() or UserAction.objects.filter(
            user=request.user,
            target_user=target_user,
            action=UserAction.ActionChoices.BLOCK,
            status=True
        ).exists():
            return Response(
                {"detail": "Unable to unfollow this user."},
                status=status.HTTP_403_FORBIDDEN
            )
           
        # Delete follow relationship
        follow_relationship.delete()
        
        return Response(
            {"detail": "Successfully unfollowed user."},
            status=status.HTTP_200_OK
        )

class FollowerListView(generics.ListAPIView):
    serializer_class = FollowerListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        username = self.kwargs['username']
        
        # Check if user exists
        user = CustomUser.objects.filter(username=username).first()
        
        if not user:
            # Return empty queryset if user not found
            return Follower.objects.none()
        
        return Follower.objects.filter(
            following__username=username
        ).select_related('follower')

    def list(self, request, *args, **kwargs):
        username = self.kwargs['username']
        
        # Check if user exists
        user = CustomUser.objects.filter(username=username).first()
        
        if not user:
            return Response(
                {"detail": "User not found with this username."},
                status=status.HTTP_404_NOT_FOUND
            )
            
        return super().list(request, *args, **kwargs)

class FollowingListView(generics.ListAPIView):
   serializer_class = FollowerListSerializer
   permission_classes = [permissions.AllowAny]

   def get_queryset(self):
    username = self.kwargs['username']
    
    # Check if user exists
    user = CustomUser.objects.filter(username=username).first()
    
    if not user:
        return Follower.objects.none()
    
    return Follower.objects.filter(
        follower__username=username
    ).select_related('following')

   def list(self, request, *args, **kwargs):
       username = self.kwargs['username']
       
       # Check if user exists
       user = CustomUser.objects.filter(username=username).first()
       
       if not user:
           return Response(
               {"detail": "User not found with this username."},
               status=status.HTTP_404_NOT_FOUND
           )
           
       return super().list(request, *args, **kwargs)

class UserActionView(generics.CreateAPIView, generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserActionSerializer

    @transaction.atomic
    def post(self, request, username):
        target_user = get_object_or_404(CustomUser, username=username)
        
        if request.user == target_user:
            return Response(
                {"detail": "Cannot perform actions on yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        action = request.data.get('action')
        if action not in [UserAction.ActionChoices.HIDE, UserAction.ActionChoices.BLOCK]:
            return Response(
                {"detail": "Invalid action."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check for existing action
        existing_action = UserAction.objects.filter(
            user=request.user,
            target_user=target_user,
            action=action
        ).first()

        if existing_action:
            if existing_action.status:
                return Response(
                    {"detail": f"You have already {action.lower()}ed this user."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                existing_action.status = True
                existing_action.save()
                serializer = self.get_serializer(existing_action)
                return Response(serializer.data, status=status.HTTP_200_OK)

        # Create new action
        serializer = self.get_serializer(
            data={'action': action},
            context={'request': request, 'target_user': target_user}
        )
        serializer.is_valid(raise_exception=True)
        action_obj = serializer.save()

        # # Handle block consequences
        # if action == UserAction.ActionChoices.BLOCK:
        #     Follower.objects.filter(
        #         follower=request.user,
        #         following=target_user
        #     ).delete()
        #     Follower.objects.filter(
        #         follower=target_user,
        #         following=request.user
        #     ).delete()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, username):
        # Validate that the target username exists in the database
        try:
            target_user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get the action from request body
        action = request.data.get('action')

        # Validate action
        if not action or action not in UserAction.ActionChoices.values:
            return Response(
                {"detail": "Invalid or missing action."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check for existing action
        try:
            # print(request.user.id, target_user.id, action)
            user_action = UserAction.objects.get(
                user=request.user.id,
                target_user=target_user.id,
                action=action,
                status=True
            )
        except UserAction.DoesNotExist:
            return Response(
                {"detail": "No active action found for this user and action."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Soft delete by setting status to False
        user_action.status = False
        user_action.save()

        return Response({"message":"Action deleted successfully"}
            ,status=status.HTTP_204_NO_CONTENT)
    
class UserActionListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserActionSerializer

    def get_queryset(self):
        return UserAction.objects.filter(
            user=self.request.user,
            status=True
        ).select_related('target_user')