from django.db import models
from django.conf import settings

# Create your models here.
class Note(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    title = models.CharField(max_length=64)
    author = models.CharField(max_length=128, null=True, blank=True)
    book_title = models.CharField(max_length=128, null=True, blank=True)
    publisher = models.CharField(max_length=64, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    content = models.TextField(max_length=8500)
    timestamp = models.DateTimeField(auto_now_add=True)
    