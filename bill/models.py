from django.db import models
from django.conf import settings
from stuff.models import Room, Service
from mypage.models import Contract,Company

# Create your models here.

class Booking (models.Model):
    person = models.ForeignKey(
        settings.AUTH_USER_MODEL
        )
    s_date = models.DateTimeField(
        'День заезда'
        )
    e_date = models.DateTimeField(
        'День выезда'
        )
    room = models.ForeignKey(Room)
    is_delete = models.NullBooleanField(
        'Удалена',
        null=True
        )
    child = models.SmallIntegerField(
        'Количество детей'
        )
    number_peoples = models.SmallIntegerField(
        'Количество людей'
        )
    contract=models.ForeignKey(
        Contract,
        null=True,
        blank=True
        )
    date=models.DateTimeField(
        'Время бронирования',
        auto_now_add=True
        )
    price=models.IntegerField(
        'Цена',
        null=True
        )
    company=models.ForeignKey(
        Company,
        null=True,
        blank=True
        )
    
    def __str__(self):
        return str(self.person)+str(self.date.strftime(" %d.%m.%Y %I:%M %p"))
    
class Service_order (models.Model):
    person = models.ForeignKey(
        settings.AUTH_USER_MODEL
        )
    service = models.ForeignKey(
        Service
        )
    booking=models.ForeignKey(
        Booking
        )
    date = models.DateTimeField(
        'Время заказа',
        auto_now_add=True
        )
    price=models.IntegerField(
        'Цена',
        null=True
        )
    is_delete = models.NullBooleanField(
        'Удалена',
        null=True
        )
    def __str__(self):
        return str(self.person)+str(self.date.strftime(" %d.%m.%Y %I:%M %p"))
