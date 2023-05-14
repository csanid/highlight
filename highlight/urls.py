from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("add", views.add, name="add"),
    path("search", views.search, name="search"),
    path("notes/<int:note_id>", views.get_note, name="get_note"),    
]
