from django.db import models
from django.conf import settings

# Create your models here.
class Note(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    author = models.CharField(max_length=128, blank=True)
    book_title = models.CharField(max_length=128, blank=True)
    publisher = models.CharField(max_length=64, blank=True)
    year = models.IntegerField(blank=True)
    content = models.TextField(max_length=8500)
    timestamp = models.DateField(auto_now_add=True)
    