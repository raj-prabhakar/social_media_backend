from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    
    # Additional fields can be added here as needed
    # bio = models.TextField(max_length=500, blank=True)  # This is removed based on your requirement
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'
