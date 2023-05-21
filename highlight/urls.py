from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("add", views.add, name="add"),
    path("edit/<int:note_id>", views.edit, name="edit"),    
    path("notes/<int:note_id>", views.get_note, name="get_note"),    
    path("delete/<int:note_id>", views.delete, name="delete"),
    path("search", views.search, name="search"),
    path("settings", views.settings, name="settings"),
    path("change_password", 
         auth_views.PasswordChangeView.as_view(
             template_name="settings.html",
             success_url="/"
         ), 
         name="change_password"),
    path("delete_account", views.delete_account, name="delete_account")
]
