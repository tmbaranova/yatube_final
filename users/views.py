from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models.signals import post_save
from django.dispatch import receiver

from .forms import CreationForm, ProfileForm
from .models import Profile
from posts.models import Chat, Message

User = get_user_model()


class SignUpView(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"


@login_required
def add_info(request):
    profile = Profile.objects.get_or_create(user=request.user)[0]
    form = ProfileForm(request.POST or None, files=request.FILES or None, instance=profile)
    if not form.is_valid():
        return render(request, 'add_info.html', {'form': form})

    form.save()
    return redirect('posts:profile', username=request.user.username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    admin = User.objects.filter(is_superuser = True)[0]
    if created:
        Profile.objects.create(user=instance)
        chat = Chat.objects.create(user1=admin, user2=instance)
        Message.objects.create(sender=admin,
                               recipient=instance,
                               text='hello',
                               chat=chat
                               )










