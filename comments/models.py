from django.db import models
from django.conf import settings
from django.contrib import admin



class Comment (models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL
        )
    title=models.CharField(
        'Заголовок',
        max_length=140
        )
    comment = models.CharField(
        'Отзыв',
        max_length=1000
        )
    date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
        )
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
    

class CommentAdmin(admin.ModelAdmin):
    list_display=('user','date')

class Rating (models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL
        )
    comment=models.ForeignKey(
        Comment,
        verbose_name="Заголовок коментария"
        )
    date = models.DateTimeField(
        'Дата оценки',
        auto_now_add=True
        )
    value=models.IntegerField(
        'Оценка'
        )


    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
