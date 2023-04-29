from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, NoteForm

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))    
    # context variables for authenticated user: display of recent cards
    # o en realidad que se muestren todas ordenadas por más recientes
    return render(request, "highlight/index.html")

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome back {username}!")
                return HttpResponseRedirect(reverse("index"))
            else:
                # or messages.error(request, "Invalid credentials")
                return render (request, "highlight/login.html", {
                    "message": "Invalid username or password"
                })
    form = LoginForm()
    return render(request, "highlight/login.html", {
        "form": form
    })

@login_required
def logout(request):
    logout(request)
    return render(request, "highlight/login.html", {
        "message": "Successfully logged out"
    })

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return render(request, "highlight.index.html", {
                "message": "You have successfully registered"
            })  
    form = RegisterForm()
    return render(request, "highlight/register.html", { 
        "form": form 
    })

@login_required
def add(request):
    # if request.method == "POST":
        # validate and add note
    return render(request, "highlight/add.html")

@login_required
def edit(request):
    return render(request, "highlight/edit.html")

@login_required
def delete(request):
    return render(request, "highlight/index.html")

@login_required
def search(request):
    return render(request, "highlight/search.html")
