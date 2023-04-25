from django.shortcuts import render
from django.http import HttpResponse
from .forms import NoteForm

def index(request):
    return render(request, "highlight/index.html")

def login(request):
    # if request.method == "POST":
        # some code 
        # return decorator? ver cómo
    return render(request, "highlight/login.html")

def logout(request):
    return render(request, "highlight/login.html")

def register(request):
    # if request.method == "POST":
        # register user
        # show alert
        # log in user                
    return render(request, "highlight/register.html")

def add(request):
    # if request.method == "POST":
        # validate and add note
    return render(request, "highlight/add.html")

def edit(request):
    return render(request, "highlight/edit.html")

def remove(request):
    return render(request, "highlight/remove.html")

def search(request):
    return render(request, "highlight/search.html")
