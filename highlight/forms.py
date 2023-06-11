from django import forms
from django.forms import ModelForm
from .models import Note
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'autofocus': 'true', 'oninvalid': 'setCustomValidity("This field is required")', 'oninput': 'setCustomValidity("")'})
    )    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'oninvalid': 'setCustomValidity("This field is required")', 'oninput': 'setCustomValidity("")'})
    )

class CustomPasswordChangeForm(PasswordChangeForm):
        
    def clean_new_password2(self):
        old_password = self.cleaned_data.get("old_password")
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 != new_password2:
            raise ValidationError("The new passwords do not match")
        if old_password == new_password1:
            raise ValidationError("The new password should be different from the old one")
        return new_password2 
    
class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ["title", "author", "book_title", "publisher", "year", "content"]
        widgets = {
          'title': forms.TextInput(attrs={'oninvalid': 'setCustomValidity("This field is required")', 'oninput': 'setCustomValidity("")'}),
          'content': forms.Textarea(attrs={'rows': '3', 'id': 'content', 'oninvalid': 'setCustomValidity("This field is required")', 'oninput': 'setCustomValidity("")'}),
        }
    
    def clean(self):
        super(NoteForm, self).clean()
        title = self.cleaned_data.get("title")
        content = self.cleaned_data.get("content")
        if title == "" or content == "":
            raise forms.ValidationError("This field is required")
        return self.cleaned_data   
            