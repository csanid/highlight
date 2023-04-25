from django.db import models

# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=64)
    author = models.CharField(max_length=128, blank=True)
    book_title = models.CharField(max_length=128, blank=True)
    publisher = models.CharField(max_length=64, blank=True)
    year = models.IntegerField(blank=True)
    content = models.CharField(max_length=8500)
    timestamp = models.DateField(auto_now_add=True)
    