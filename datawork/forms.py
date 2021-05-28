from django import forms
from .models import *


class UserSignup(forms.ModelForm):
    class Meta:
        exclude = ('city', 'state', 'language', 'dp', 'cover_image', 'date_of_creation')
        model = User


class Dpupdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['dp']


class Userupdate(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('dp', 'cover_image', 'date_of_creation')
