from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, AccessKey

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username','email', 'password1', 'password2', 'user_type')

class AccessKeyForm(forms.ModelForm):
    class Meta:
        model = AccessKey
        fields = ['status', 'expiry_date']
