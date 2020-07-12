from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField() # added cuz its not default
    class Meta:
        """Meta for change some settings
        connect UserRegisterForm with User(Django Lib)
        fields = means update which fields in ORM"""
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    """ModelForm https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/"""
    email = forms.EmailField() # add attribute for email
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']