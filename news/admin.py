from django.contrib import admin

# Register your models here.
from .models import Article, WebsiteUser, Comment, Like, Dislike

admin.site.register(Article)
admin.site.register(WebsiteUser)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Dislike)