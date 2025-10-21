from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django import forms

class Register(UserCreationForm):
    first_name=forms.CharField(max_length=30)
    last_name=forms.CharField(max_length=40)
    email=forms.EmailField()

    class Meta:
        models=CustomUser
        fields=['first_name','last_name','email','phone_number','password1','password2']