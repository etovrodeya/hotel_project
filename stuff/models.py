from django.db import models

class Room (models.Model):
    housing = models.SmallIntegerField(
        'Корпус'
        )
    floor = models.SmallIntegerField(
        'Этаж'
        )
    number = models.SmallIntegerField(
        'Номер'
        )
    per_night = models.SmallIntegerField(
        'Стоимость за ночь'
        )
    number_beds = models.SmallIntegerField(
        'Количество спальных мест'
        )
    STYLE_CHOICES=(
        ('budget','budget'),
        ('business','business'),
        ('lux','lux')
        )
    style=models.CharField(
            'Класс аппартаментов',
            max_length=15,
            choices=STYLE_CHOICES
            )
    def __str__(self):
        return str(self.housing)+str(self.floor)+str(self.number)

class Service (models.Model):
    name = models.CharField(
        'Название услуги',
        max_length=50
        )
    description = models.TextField(
        'Описание услуги'
        )
    apiece = models.SmallIntegerField(
        'Цена за услугу'
        )
    def __str__(self):
        return self.name
