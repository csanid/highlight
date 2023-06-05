from django.urls import path
# from django.contrib.auth import views as auth_views
from . import views
# from .forms import MyPasswordChangeForm
# from highlight.views import MyPasswordChangeView

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("settings", views.settings, name="settings"),
    path("change_password", views.change_password, name="change_password"),
    path("delete_account", views.delete_account, name="delete_account"),
    path("add", views.add, name="add"),
    path("edit/<int:note_id>", views.edit, name="edit"),    
    path("delete/<int:note_id>", views.delete, name="delete"),
    path("search", views.search, name="search"),
    path("notes/<int:note_id>", views.get_note, name="get_note"),    
]
