from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("add_info/", views.add_info, name="add_info"),
    path("all_users/", views.show_all_users, name="show_all_users"),
    path("all_groups/", views.show_all_groups, name="show_all_groups"),
]
