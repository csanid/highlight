# Generated by Django 4.2 on 2023-05-04 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('author', models.CharField(blank=True, max_length=128, null=True)),
                ('book_title', models.CharField(blank=True, max_length=128, null=True)),
                ('publisher', models.CharField(blank=True, max_length=64, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('content', models.TextField(max_length=8500)),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
