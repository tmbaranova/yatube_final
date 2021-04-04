from django.contrib import admin

from .models import Group, Post, Comment, Follow, Like, Dislike, Chat, Message


class PostAdmin(admin.ModelAdmin):
    list_display = ('text', 'pub_date', 'author', 'group', 'is_pinned')
    list_filter = ("pub_date", 'author', 'group')
    search_fields = ("text",)
    empty_value_display = "-пусто-"


class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description')
    list_filter = ("title", )
    empty_value_display = "-пусто-"


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'text', 'created')
    list_filter = ("author", "post", )
    empty_value_display = "-пусто-"


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    list_filter = ("author", "user",)
    empty_value_display = "-пусто-"


class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'publication')
    empty_value_display = "-пусто-"


class DislikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'publication')
    empty_value_display = "-пусто-"


class ChatAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2')
    empty_value_display = "-пусто-"


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'text')
    empty_value_display = "-пусто-"


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Dislike, LikeAdmin)
admin.site.register(Chat, ChatAdmin)
