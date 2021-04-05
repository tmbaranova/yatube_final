from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Название группы',
                             help_text='Введите название группы')
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Заголовок',
                            help_text='Введите заголовок')
    text = models.TextField(blank=False, verbose_name='Текст',
                            help_text='Введите текст')
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               blank=True, null=True,
                               related_name="posts")
    group = models.ForeignKey(Group, blank=True, null=True,
                              on_delete=models.SET_NULL, related_name="posts",
                              verbose_name='Группа для поста',
                              help_text='Выберите группу'
                              )
    image = models.ImageField(upload_to='users/', blank=True, null=True)
    is_pinned = models.BooleanField(default=False)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]


class Comment (models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             blank=False, null=False,
                             related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               blank=True, null=True,
                               related_name="comments")
    text = models.TextField(blank=False, verbose_name='Текст',
                            help_text='Введите комментарий')
    created = models.DateTimeField("date published", auto_now_add=True)
    is_readed = models.BooleanField(default=False)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True, related_name="follower")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               blank=True, null=True, related_name="following")
    is_readed = models.BooleanField(default=False)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True, related_name="liker")
    publication = models.ForeignKey(Post, on_delete=models.CASCADE,
                               blank=True, null=True, related_name="like")
    is_readed = models.BooleanField(default=False)


class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True, related_name="disliker")
    publication = models.ForeignKey(Post, on_delete=models.CASCADE,
                               blank=True, null=True, related_name="dislike")
    is_readed = models.BooleanField(default=False)


class Chat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True, related_name="chat1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True, related_name="chat2")


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True, related_name="message_send")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True, related_name="message_receive")
    text = models.TextField(blank=False, verbose_name='Текст',
                            help_text='Введите текст сообщения')
    msg_date = models.DateTimeField("date published", auto_now_add=True)
    is_readed = models.BooleanField(default=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE,
                             blank=True, null=True,
                             related_name="messages")
    def __str__(self):
        return self.text[:40]




