# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bill', '0001_initial'),
        ('stuff', '0001_initial'),
        ('mypage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service_order',
            name='person',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='service_order',
            name='service',
            field=models.ForeignKey(to='stuff.Service'),
        ),
        migrations.AddField(
            model_name='booking',
            name='company',
            field=models.ForeignKey(blank=True, null=True, to='mypage.Company'),
        ),
        migrations.AddField(
            model_name='booking',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, to='mypage.Contract'),
        ),
        migrations.AddField(
            model_name='booking',
            name='person',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='booking',
            name='room',
            field=models.ForeignKey(to='stuff.Room'),
        ),
    ]
