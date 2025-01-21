# models.py
from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import CustomUser

class Follower(models.Model):
    follower = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following'
    )
    following = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        verbose_name = 'Follower'
        verbose_name_plural = 'Followers'
        indexes = [
            models.Index(fields=['follower']),
            models.Index(fields=['following']),
        ]
        ordering = ['-created_at']

    def clean(self):
        if hasattr(self, 'follower') and hasattr(self, 'following'):
            if self.follower == self.following:
                raise ValidationError("Users cannot follow themselves.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

class UserAction(models.Model):
    class ActionChoices(models.TextChoices):
        HIDE = 'HIDE', 'Hide'
        BLOCK = 'BLOCK', 'Block'

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='actions_performed'
    )
    target_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='actions_received'
    )
    action = models.CharField(
        max_length=5,
        choices=ActionChoices.choices
    )
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'target_user', 'action')
        verbose_name = 'User Action'
        verbose_name_plural = 'User Actions'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['target_user']),
            models.Index(fields=['action']),
        ]
        ordering = ['-created_at']

    def clean(self):
        if hasattr(self, 'user') and hasattr(self, 'target_user'):
            if self.user == self.target_user:
                raise ValidationError("Users cannot perform actions on themselves.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        action_past = {
            'HIDE': 'hid',
            'BLOCK': 'blocked'
        }
        past_tense = action_past.get(self.action, self.action.lower() + 'ed')
        return f"{self.user.username} {past_tense} {self.target_user.username}"