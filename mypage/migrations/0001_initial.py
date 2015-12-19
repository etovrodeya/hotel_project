# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='MpUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('email', models.EmailField(unique=True, verbose_name='Электронная почта', db_index=True, max_length=255)),
                ('country', models.CharField(null=True, blank=True, verbose_name='Страна', max_length=50)),
                ('city', models.CharField(null=True, blank=True, verbose_name='Город', max_length=50)),
                ('total_money', models.IntegerField(null=True, blank=True, verbose_name='Баланс')),
                ('firstname', models.CharField(null=True, blank=True, verbose_name='Имя', max_length=40)),
                ('lastname', models.CharField(null=True, blank=True, verbose_name='Фамилия', max_length=40)),
                ('middlename', models.CharField(null=True, blank=True, verbose_name='Отчество', max_length=40)),
                ('sex', models.CharField(choices=[('male', 'male'), ('female', 'female')], blank=True, max_length=6)),
                ('date_of_birth', models.DateField(null=True, blank=True, verbose_name='Дата рождения')),
                ('register_date', models.DateField(verbose_name='Дата регистрации', auto_now_add=True)),
                ('is_admin', models.BooleanField(verbose_name='Суперпользователь', default=False)),
                ('staff', models.CharField(choices=[('client', 'client'), ('manager', 'manager')], blank=True, max_length=15)),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100, verbose_name='Название компании', unique=True)),
                ('country', models.CharField(verbose_name='Страна', max_length=50)),
                ('city', models.CharField(verbose_name='Город', max_length=50)),
                ('mailadress', models.CharField(verbose_name='Почтовый адресс', max_length=200)),
            ],
            options={
                'verbose_name': 'Компания',
                'verbose_name_plural': 'Компании',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('contract_number', models.IntegerField(verbose_name='Номер контракта', serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='Название контракта', max_length=50)),
                ('number_people', models.SmallIntegerField(verbose_name='Количество людей')),
                ('booking_discount', models.SmallIntegerField(verbose_name='Скидка на бронирование')),
                ('service_discount', models.SmallIntegerField(verbose_name='Скидка на дополнительные услуги')),
                ('s_date', models.DateField(verbose_name='Дата заключения контракта')),
                ('e_date', models.DateField(verbose_name='Действителен до')),
                ('is_active', models.BooleanField(verbose_name='Действителен?')),
                ('company', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True, to='mypage.Company')),
            ],
            options={
                'verbose_name': 'Контракт',
                'verbose_name_plural': 'Контракты',
            },
        ),
        migrations.AddField(
            model_name='mpuser',
            name='company',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True, to='mypage.Company'),
        ),
        migrations.AddField(
            model_name='mpuser',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', blank=True, to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups', related_name='user_set'),
        ),
        migrations.AddField(
            model_name='mpuser',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', blank=True, to='auth.Permission', help_text='Specific permissions for this user.', verbose_name='user permissions', related_name='user_set'),
        ),
    ]
