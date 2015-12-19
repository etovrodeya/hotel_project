from django.contrib import admin
from .models import Comment, CommentAdmin,Rating



admin.site.register(Comment,CommentAdmin)
admin.site.register(Rating)
