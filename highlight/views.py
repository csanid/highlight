from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import RegisterForm, CustomPasswordChangeForm, LoginForm, NoteForm
from .models import Note

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))    
    form = NoteForm
    user = request.user
    notes = user.notes.all().order_by("-timestamp")
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
    return HttpResponseRedirect(reverse("login"))

def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST":        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            note_form = NoteForm
            return render(request, "highlight/index.html", {
                "message": "You have successfully registered",
                "form": note_form
            })      
    return render(request, "highlight/register.html", { 
        "form": form 
    })

@login_required
def settings(request):
    if request.method == "GET":        
        return render(request, "highlight/settings.html")

@login_required
def change_password(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated")
            return HttpResponseRedirect(reverse("settings"))   
        else:
            return render(request, "highlight/password_update.html", {
                "form": form
            })
    form = CustomPasswordChangeForm(request.user)
    return render(request, "highlight/password_update.html", {
        "form": form
    })

@login_required
def delete_account(request):
    if request.method == "GET":
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted")
        return HttpResponseRedirect(reverse("login"))

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

@login_required
def delete(request, note_id):
    if request.method == "GET":
        Note.objects.filter(id=note_id).delete()
        return HttpResponseRedirect(reverse("index"))

@login_required
def search(request):
    if request.method == "GET":
        search_term = request.GET.get("search-bar")   
        user = request.user
        notes = user.notes.filter(
            Q(title__icontains=search_term) |
            Q(author__icontains=search_term) |
            Q(book_title__icontains=search_term) |
            Q(publisher__icontains=search_term) |
            Q(year__icontains=search_term) |
            Q(content__icontains=search_term)
        )        
        if not notes.exists():
            search_message = f"No results found for '{search_term}'"
        else:
            search_message = f"Search results for '{search_term}':"        
        form = NoteForm
        return render(request, "highlight/index.html", {
            "form": form,
            "notes": notes,
            "search_message": search_message
        })          
       
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
 