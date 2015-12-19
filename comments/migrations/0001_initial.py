# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name='Заголовок', max_length=140)),
                ('comment', models.CharField(verbose_name='Отзыв', max_length=1000)),
                ('date', models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('date', models.DateTimeField(verbose_name='Дата оценки', auto_now_add=True)),
                ('value', models.IntegerField(verbose_name='Оценка')),
                ('comment', models.ForeignKey(to='comments.Comment', verbose_name='Заголовок коментария')),
            ],
            options={
                'verbose_name': 'Оценка',
                'verbose_name_plural': 'Оценки',
            },
        ),
    ]
