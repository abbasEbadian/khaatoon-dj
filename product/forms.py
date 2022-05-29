
from django import forms
from .models import  Market

class coveruploadform(forms.ModelForm):
    class Meta:
        model = Market
        fields = ['cover']

class imageuploadform(forms.ModelForm):
    class Meta:
        model = Market
        fields = ['image']

class documentuploadform(forms.ModelForm):
    class Meta:
        model = Market
        fields = ['document']