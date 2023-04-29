from django import forms
from django.forms import ModelForm
from .models import Note
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# ver https://medium.com/swlh/how-to-style-your-django-forms-7e8463aae4fa para estilo
# ver widget textarea 

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
  
class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ["title", "author", "book_title", "publisher", "year", "content"]