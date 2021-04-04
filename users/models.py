from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(default="default.jpg", upload_to='users/', blank=False, null=False)
    info = models.TextField(blank=True, null=True)
