from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, NoteForm
from .models import Note

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))    
    form = NoteForm
    user = request.user
    notes = user.notes.all().order_by("-timestamp")
    # notes = Note.objects.filter(
        # user_id = request.user).order_by("-timestamp")
    return render(request, "highlight/index.html", {
        "form": form,
        "notes": notes        
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
                })
    return render(request, "highlight/login.html", {
        "form": form
    })

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out")
    return HttpResponseRedirect(reverse("login"))

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
def edit(request, note_id):
    note = Note.objects.get(id=note_id)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse("index"))
    # form = NoteForm(instance=note)
    # return render(request, "highlight/index.html", {
    #    "form": form              
    # })

@login_required
def delete(request):
    return render(request, "highlight/index.html")

@login_required
def search(request):
    # resultados en index con opción de "< Back" en botón o texto para volver a home
    return render(request, "highlight/search.html")

@login_required
def get_note(request, note_id):
    if request.method == "GET":
        note = get_object_or_404(Note, pk=note_id)
        data = {            
            "id": note.id,            
            "title": note.title,
            "author": note.author,
            "book_title": note.book_title,
            "publisher": note.publisher,
            "year": note.year,
            "content": note.content,
            "timestamp": note.timestamp.isoformat(),
        }
        return JsonResponse(data)
 