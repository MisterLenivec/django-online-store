from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from phonenumber_field.formfields import PhoneNumberField


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_number = PhoneNumberField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email',
                  'phone_number', 'password1', 'password2']
