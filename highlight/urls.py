from django.urls import path

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
]
