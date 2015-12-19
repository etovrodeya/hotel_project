# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('s_date', models.DateTimeField(verbose_name='День заезда')),
                ('e_date', models.DateTimeField(verbose_name='День выезда')),
                ('is_delete', models.NullBooleanField(verbose_name='Удалена')),
                ('child', models.SmallIntegerField(verbose_name='Количество детей')),
                ('number_peoples', models.SmallIntegerField(verbose_name='Количество людей')),
                ('date', models.DateTimeField(verbose_name='Время бронирования', auto_now_add=True)),
                ('price', models.IntegerField(null=True, verbose_name='Цена')),
            ],
        ),
        migrations.CreateModel(
            name='Service_order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('date', models.DateTimeField(verbose_name='Время заказа', auto_now_add=True)),
                ('price', models.IntegerField(null=True, verbose_name='Цена')),
                ('is_delete', models.NullBooleanField(verbose_name='Удалена')),
                ('booking', models.ForeignKey(to='bill.Booking')),
            ],
        ),
    ]
