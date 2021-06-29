from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from django.db.models import Q
from django.db.models import Max

from .forms import CommentForm, PostForm, GroupForm, MessageForm
from .models import Comment, Follow, Group, Post, Like, Dislike, Message, Chat


User = get_user_model()
PAGE_NUMBERS_FOR_PAGINATOR = 5


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, PAGE_NUMBERS_FOR_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'post_list':
                                              post_list, 'page': page})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    group_list = group.posts.all()
    paginator = Paginator(group_list, PAGE_NUMBERS_FOR_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html',
                  {"group": group, 'page': page})


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("posts:index")

        return render(request, 'new.html', {'form': form})

    form = PostForm()
    return render(request, 'new.html', {'form': form})


@login_required
def new_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("posts:index")

        return render(request, 'new_group.html', {'form': form})

    form = GroupForm()
    return render(request, 'new_group.html', {'form': form})


@login_required
def profile(request, username):
    author = get_object_or_404(User, username=username)
    author_posts_list = author.posts.all()
    following = author.following.all()
    follower = request.user.follower.all()
    is_follower = following.intersection(follower)
    paginator = Paginator(author_posts_list, PAGE_NUMBERS_FOR_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    chat = None
    results = Chat.objects.filter(
                Q(user1=request.user) | Q(user1=author)).filter(
        Q(user2=request.user) | Q(user2=author))
    if results:
        chat = results[0]
    return render(request, 'profile.html',
                  {"author": author, 'page': page,
                   'chat': chat, 'is_follower': is_follower})


@login_required
def post_view(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    comments = Comment.objects.filter(post=post_id)
    if post.author == request.user:
        for comment in comments:
            comment.is_readed = True
            comment.save()
    form = CommentForm()
    chat = None
    results = Chat.objects.filter(
        Q(user1=request.user) | Q(user1=post.author)).filter(Q(
        user2=request.user) | Q(user2=post.author))
    if results:
        chat = results[0]

    return render(request, 'post.html', {'post': post, 'author': post.author,
                                         'comments': comments,
                                         'form': form, 'chat': chat},)


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    if request.user != post.author:
        return redirect('posts:post', username=username, post_id=post_id)

    form = PostForm(request.POST or None, files=request.FILES or None,
                    instance=post)

    if not form.is_valid():
        return render(request, 'new.html', {'form': form, 'post': post})

    form.save()
    return redirect('posts:post', username=username, post_id=post_id)


@login_required
def post_delete(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    if request.user != post.author:
        return redirect('posts:post', username=username, post_id=post_id)
    post.delete()
    return redirect('posts:index')


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    comments = Comment.objects.filter(post=post_id)
    if post.author == request.user:
        for comment in comments:
            comment.is_readed = True
            comment.save()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('posts:post', username=username, post_id=post_id)

        return render(request, 'post.html', {'form': form,
                                             'post': post,
                                             'comments': comments})

    form = CommentForm()
    return render(request, 'post.html', {'form': form,
                                         'post': post, 'comments': comments})


@login_required
def new_events(request, username):
    unreaded_comments = Comment.objects.filter(
        post__author=request.user).filter(is_readed=False)
    for comment in unreaded_comments:
        comment.is_readed = True
        comment.save()

    new_followers = Follow.objects.filter(author=request.user).filter(
        is_readed=False)
    for follower in new_followers:
        follower.is_readed = True
        follower.save()

    new_likes = Like.objects.filter(publication__author=request.user).filter(
        is_readed=False)
    for like in new_likes:
        like.is_readed = True
        like.save()

    new_dislikes = Dislike.objects.filter(
        publication__author=request.user).filter(is_readed=False)
    for dislike in new_dislikes:
        dislike.is_readed = True
        dislike.save()

    return render(request, 'new_comments.html',
                  {'unreaded_comments': unreaded_comments,
                   'new_followers': new_followers,
                   'new_likes': new_likes,
                   'new_dislikes': new_dislikes})



@login_required
def follow_index(request):
    following_authors_posts = Post.objects.filter(
        author__following__user=request.user)
    paginator = Paginator(following_authors_posts, PAGE_NUMBERS_FOR_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'follow.html',
                  {'page': page, 'paginator': paginator})


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)

    return redirect('posts:profile', username=author)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    following = Follow.objects.filter(user=request.user, author=author)
    following.delete()

    return redirect('posts:profile', username=author)


def post_search(request):
    query = request.GET.get('query')
    if query:
        results = Post.objects.filter(
                Q(text__icontains=query) |
                Q(author__username__icontains=query) |
                Q(group__title__icontains=query))

        return render(request, 'search.html', {'query': query, 'results': results})
    return render(request, 'search.html')


@login_required
def like(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    dislike = Dislike.objects.filter(user=request.user, publication=post)
    if not dislike:
        like = Like.objects.get_or_create(user=request.user, publication=post)
        if like[1]==False:
            like[0].delete()
    prewious_url = request.META.get('HTTP_REFERER')
    return redirect(prewious_url)


@login_required
def dislike(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    like = Like.objects.filter(user=request.user, publication=post)
    if not like:
        dislike = Dislike.objects.get_or_create(
            user=request.user, publication=post)
        if dislike[1]==False:
            dislike[0].delete()
    prewious_url = request.META.get('HTTP_REFERER')
    return redirect(prewious_url)


@login_required
def chatrooms(request):
    chatrooms = Chat.objects.filter(
            Q(user1=request.user) | Q(user2=request.user)).annotate(
        max_data=Max('messages__msg_date')).order_by("-max_data")

    unreaded_messages = Message.objects.filter(
        chat__in=chatrooms).filter(
        is_readed=False).filter(recipient=request.user)

    return render(request, 'chatrooms.html',
                  {'chatrooms': chatrooms})

@login_required
def create_chat(request, username):
    recipient = get_object_or_404(User, username=username)
    form = MessageForm()
    chat1 = Chat.objects.filter(user1=request.user).filter(user2=recipient)
    chat2 = Chat.objects.filter(user2=request.user).filter(user1=recipient)
    if chat1 or chat2:
        prewious_url = request.META.get('HTTP_REFERER')
        return redirect(prewious_url)

    chat = Chat.objects.create(user1=request.user, user2=recipient)
    return render(request, 'chat.html', {'chat': chat, 'form': form})


@login_required
def show_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user != chat.user1 and request.user != chat.user2:
        return redirect('posts:index')
    form = MessageForm()
    messages = Message.objects.filter(chat=chat).order_by("-msg_date")
    for message in messages:
        if message.recipient == request.user:
            message.is_readed = True
            message.save()
    paginator = Paginator(messages, PAGE_NUMBERS_FOR_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'chat.html',
                  {'chat': chat, 'form': form,
                   'page': page, 'messages': messages})


@login_required
def message(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user != chat.user1 and request.user != chat.user2:
        return redirect('posts:index')
    if request.user != chat.user1:
        recipient = chat.user1
    else:
        recipient = chat.user2

    messages = Message.objects.filter(chat=chat).order_by("-msg_date")

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.chat = chat
            message.save()
            chat.last_message = message
            chat.save()
            return redirect('posts:chat', chat_id=chat.id)

        return render(request, 'chat.html',
                      {'form': form, 'chat': chat, 'messages':messages})

    form = MessageForm()
    return render(request, 'chat.html',
                  {'form': form, 'chat': chat, 'messages': messages})
