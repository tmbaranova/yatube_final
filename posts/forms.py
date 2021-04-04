from django.forms import ModelForm
from django import forms

from .models import Comment, Post, Group, Message


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['group', 'title', 'text', 'image']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'slug', 'description']


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['text']


