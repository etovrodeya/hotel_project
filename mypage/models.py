from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,email,password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user=self.model(
            email=UserManager.normalize_email(email),
            )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password):
        user=self.create_user(email=email, password=password)
        user.is_admin=True
        user.is_superuser=True
        user.is_active=True
        user.save(using=self._db)
        return user

class Company (models.Model):
    name = models.CharField(
        'Название компании',
        max_length=100,
        unique=True
        )
    country = models.CharField(
        'Страна',
        max_length=50
        )
    city = models.CharField(
        'Город',
        max_length=50
        )
    mailadress = models.CharField(
        'Почтовый адресс',
        max_length=200
        )
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

class Contract (models.Model):
    contract_number = models.IntegerField(
        'Номер контракта',
        primary_key=True
        )
    name = models.CharField(
        'Название контракта',
        max_length=50
        )
    number_people = models.SmallIntegerField(
        'Количество людей'
        )
    booking_discount = models.SmallIntegerField(
        'Скидка на бронирование'
        )
    service_discount = models.SmallIntegerField(
        'Скидка на дополнительные услуги'
        )
    s_date = models.DateField(
        'Дата заключения контракта'
        )
    e_date = models.DateField(
        'Действителен до'
        )
    is_active = models.BooleanField(
        'Действителен?'
        )
    company = models.ForeignKey(
        Company,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
        )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'    

class MpUser (AbstractBaseUser, PermissionsMixin):
    email=models.EmailField(
        'Электронная почта',
        max_length=255,
        unique=True,
        db_index=True
        )
    company = models.ForeignKey(
        Company,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
        )
    country = models.CharField(
        'Страна',
        blank=True,
        null=True,
        max_length=50
        )
    city = models.CharField(
        'Город',
        blank=True,
        null=True,
        max_length=50
        )
    total_money = models.IntegerField(
        'Баланс',
        blank=True,
        null=True
        )
    firstname = models.CharField(
        'Имя',
        max_length=40,
        null=True,
        blank=True
    )
    lastname = models.CharField(
        'Фамилия',
        max_length=40,
        null=True,
        blank=True
    )
    middlename = models.CharField(
        'Отчество',
        max_length=40,
        null=True,
        blank=True
    )
    SEX_CHOICES = (
        ('male','male'),
        ('female','female')
        )
    sex=models.CharField(
        max_length=6,
        choices=SEX_CHOICES,
        blank=True
        )
    date_of_birth = models.DateField(
        'Дата рождения',
        null=True,
        blank=True
    )
    register_date = models.DateField(
        'Дата регистрации',
        auto_now_add=True
        )
    is_admin = models.BooleanField(
        'Суперпользователь',
        default=False
    )
    STAFF_CHOICES=(
        ('client','client'),
        ('manager','manager'),
        )
    staff=models.CharField(
        max_length=15,
        choices=STAFF_CHOICES,
        blank=True
        )
    def get_full_name(self):
        return self.email
    
    @property
    def is_staff(self):
        return self.is_admin

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
