import hashlib
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    about_me = models.TextField(max_length=500, blank=True)
    img_file = models.ImageField(upload_to='static/images', blank=True)
    comments = models.ManyToManyField(
        'self',
        related_name='related_to',
        symmetrical=False,
        blank=True,
        through='Comentary'
    )

class News(models.Model):
    __tablename__ = 'news'
    title = models.TextField(max_length=64, blank=False)
    index_body = models.TextField(max_length=256, blank=False)
    body = models.TextField(max_length=2048, blank=False)
    img_file = models.ImageField(upload_to='static/images', blank=True)
    news_file = models.FileField(upload_to='static/newstext', blank=True)
    timestamp = models.DateTimeField(default=datetime.utcnow)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.ManyToManyField(
        'self',
        related_name='related_to',
        symmetrical=False,
        blank=True,
        through='Comentary'
    )


class Comentary(models.Model):
    __tablename__ = 'comments'
    body = models.TextField(max_length=512, blank=False)
    timestamp = models.DateField(datetime.utcnow)
    author_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    news_id = models.ForeignKey(News, on_delete=models.CASCADE)


class Files(models.Model):
    __tablename__ = 'files'
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='static/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
