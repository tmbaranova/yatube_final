from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path("", views.index, name='index'),
    path("chatrooms", views.chatrooms, name = "chatrooms"),
    path("chat/<str:username>/create", views.create_chat, name='create_chat'),
    path("chat/<int:chat_id>", views.show_chat, name="chat"),
    path("chat/<int:chat_id>/message/", views.message, name="message"),
    path('search/', views.post_search, name='post_search'),
    path("follow/", views.follow_index, name="follow_index"),
    path("<str:username>/follow/", views.profile_follow,
         name="profile_follow"),
    path("<str:username>/unfollow/", views.profile_unfollow,
         name="profile_unfollow"),
    path("group/<slug>/", views.group_posts, name='group_posts'),
    path("new", views.new_post, name='new_post'),
    path("new_group", views.new_group, name='new_group'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    path('<str:username>/<int:post_id>/edit/', views.post_edit,
         name='post_edit'),
    path('<str:username>/<int:post_id>/delete/', views.post_delete,
         name='post_delete'),
    path("<str:username>/<int:post_id>/comment/", views.add_comment,
         name="add_comment"),
    path("<str:username>/<int:post_id>/like/", views.like,
         name="like"),
    path("<str:username>/<int:post_id>/dislike/", views.dislike,
         name="dislike"),
    path("<str:username>/new_events", views.new_events,
         name="new_events"),
    path("404", views.page_not_found, name='page_not_found'),
    path("500", views.server_error, name='server_error'),
]
