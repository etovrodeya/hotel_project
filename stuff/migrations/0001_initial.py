# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('housing', models.SmallIntegerField(verbose_name='Корпус')),
                ('floor', models.SmallIntegerField(verbose_name='Этаж')),
                ('number', models.SmallIntegerField(verbose_name='Номер')),
                ('per_night', models.SmallIntegerField(verbose_name='Стоимость за ночь')),
                ('number_beds', models.SmallIntegerField(verbose_name='Количество спальных мест')),
                ('style', models.CharField(choices=[('budget', 'budget'), ('business', 'business'), ('lux', 'lux')], verbose_name='Класс аппартаментов', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='Название услуги', max_length=50)),
                ('description', models.TextField(verbose_name='Описание услуги')),
                ('apiece', models.SmallIntegerField(verbose_name='Цена за услугу')),
            ],
        ),
    ]
