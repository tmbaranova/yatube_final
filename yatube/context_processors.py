import datetime as dt
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Count

from posts.models import Group, Post, Comment, Follow, Like, Dislike, Message

User = get_user_model()


def year(request):
    now_year = dt.datetime.today().year
    return {'year': now_year}


def new_authors(request):
    new_authors = User.objects.order_by("-date_joined")[:3]

    return {'new_authors': new_authors}


def popular(request):
    annotated_authors = User.objects.annotate(
        likes_count=Count('posts__likes')).order_by("-likes_count")[:3]
    annotated_groups = Group.objects.annotate(
        posts_count=Count('posts')).order_by("-posts_count")[:3]
    return {'popular_authors': annotated_authors,
            'popular_groups': annotated_groups}


def unreaded_comments(request):
    if request.user.is_authenticated:
        unreaded_comments = Comment.objects.filter(post__author=request.user).filter(is_readed=False)
        new_followers = Follow.objects.filter(author=request.user).filter(is_readed=False)
        new_likes = Like.objects.filter(publication__author=request.user).filter(is_readed=False)
        new_dislikes = Dislike.objects.filter(publication__author=request.user).filter(is_readed=False)
        new_events_count = unreaded_comments.count() + new_followers.count() + new_likes.count() + new_dislikes.count()
        return {'new_events_count': new_events_count }
    else:
        return {'new_events_count': None}

def new_messages(request):
    if request.user.is_authenticated:
        new_messages = Message.objects.filter(recipient=request.user).filter(is_readed=False)
        new_messages_count = new_messages.count()
        return {'new_messages_count': new_messages_count }
    else:
        return {'new_messages_count': None}

