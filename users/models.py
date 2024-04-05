from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars', default='avatars/default.png')
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'


class SMSCodes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=7)
    created_at = models.DateTimeField(auto_now_add=True)
