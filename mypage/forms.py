from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField,UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.template import RequestContext
from mypage.models import MpUser


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Подтверждение',
        widget=forms.PasswordInput
    )

    def clean_email(self):
        email=self.cleaned_data["email"]
        try:
            MpUser._default_manager.get(email=email)
        except MpUser.DoesNotExist:
            return email
        raise forms.ValidationError('Такой email уже существует')
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароль и подтверждение не совпадают')
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.total_money=0
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields=['email']


class cUserChangeForm(UserChangeForm):

    def __init__( self, *args, **kwargs ):
        super( cUserChangeForm, self ).__init__( *args, **kwargs )
        self.fields['password'] = self.instance.password

    class Meta:
        model = get_user_model()
        fields = ['email', ]

class LoginForm(forms.Form):
    email = forms.CharField(label=u'Email')
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        if not self.errors:
            user = auth.authenticate(email=cleaned_data['email'], password=cleaned_data['password'])
            if user is None:
                raise forms.ValidationError(u'Имя пользователя и пароль не подходят')
            self.user = user
        return cleaned_data

    def get_user(self):
        return self.user or None

class RegistrationForm(forms.Form):
    login=forms.CharField(label='asd',max_length=100,error_messages={'required': 'Укажите логин'})
    password=forms.CharField(label='Пароль',widget=forms.PasswordInput(),error_messages={'required': 'Укажите пароль'})
    password_again = forms.CharField(label='Пароль (еще раз)',widget=forms.PasswordInput(),error_messages={'required': 'Укажите пароль еще раз'})
    def clean(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('password_again'):
            raise forms.ValidationError('Пароли должны совпадать!')
        return self.cleaned_data

class MyPageForm(forms.ModelForm):
  class Meta:
    model = MpUser
    fields=['firstname','middlename','lastname','sex','company','country','city','date_of_birth']

class AddMoneyForm(forms.ModelForm):
    class Meta:
        model=MpUser
        fields=['total_money']
