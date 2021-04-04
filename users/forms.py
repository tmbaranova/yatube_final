from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Profile

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'info')

