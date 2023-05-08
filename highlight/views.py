from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, NoteForm

def index(request):
    # if not request.user.is_authenticated:
        # return HttpResponseRedirect(reverse("login"))    
    # context variables for authenticated user: display of recent cards
    # o en realidad que se muestren todas ordenadas por más recientes
    title = "Quotes"
    content = "'Speak the truth, and you shall not be friendless while I live.'"
    form = NoteForm
    return render(request, "highlight/index.html", {
        "form" : form,
        "title": title, 
        "content": content
    })

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":        
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                # messages.success(request, f"Welcome back, {username.capitalize()}!")
                return HttpResponseRedirect(reverse("index"))
            else:
                messages.error(request, "Invalid username or password")
                return render(request, "highlight/login.html", {
                    "form": form
                    # "message": "Invalid username or password"
                })
    return render(request, "highlight/login.html", {
        "form": form
    })

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out")
    return HttpResponseRedirect(reverse("login_view"))
    # return render(request, "highlight/login.html", {
    #     "message": "You have successfully logged out"
    #})

def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST":        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return render(request, "highlight/index.html", {
                "message": "You have successfully registered"
            })      
    return render(request, "highlight/register.html", { 
        "form": form 
    })

@login_required
def add(request):
    
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user_id = request.user
            note.save()
            return HttpResponseRedirect(reverse("index"))
        
@login_required
def edit(request):
    return render(request, "highlight/edit.html")

@login_required
def delete(request):
    return render(request, "highlight/index.html")

@login_required
def search(request):
    return render(request, "highlight/search.html")
