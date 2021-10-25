from django.db import models
from django.contrib.auth.models import User
from .enums import Category
from django.utils import timezone
import uuid

class Article(models.Model):
    content = models.TextField(max_length=1500)
    title = models.TextField(max_length=1500)
    pub_date = models.DateField('Date Published', default=timezone.now)
    category = models.TextField(choices=Category.choices(), max_length=100, null=True)
    ident = models.CharField(max_length=100, blank=True, default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.title

class WebsiteUser(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fave_categories = models.TextField(max_length=150,
                                       null = True,
                                       blank = True)
    DOB = models.DateField('Date of Birth', null=True, blank=True)
    image = models.ImageField(upload_to='profile_pics', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    user = models.ForeignKey(WebsiteUser, on_delete=models.CASCADE)
    in_reply_to = models.ForeignKey('self', null=True, blank=True, default=None, on_delete=models.CASCADE)
    text = models.TextField(max_length=1500)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ident = models.CharField(max_length=100, blank=True, default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.text

class Like(models.Model):
    user = models.ForeignKey(WebsiteUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ident = models.CharField(max_length=100, blank=True, default=uuid.uuid4, unique=True)
    def __str__(self):
        return "1"

class Dislike(models.Model):
    user = models.ForeignKey(WebsiteUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ident = models.CharField(max_length=100, blank=True, default=uuid.uuid4, unique=True)
    def __str__(self):
        return "-1"