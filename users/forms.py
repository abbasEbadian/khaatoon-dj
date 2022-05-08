from django import forms
from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from .models import CustomUser 
 
from django.contrib.auth.forms import ReadOnlyPasswordHashField
class CustomUserCreationForm(UserCreationForm):    
    class Meta:        
        model = CustomUser        
        fields = ('email', 'username') 


class CustomUserChangeForm(UserChangeForm):
    """Overriding visible fields."""
    class Meta:
        model = CustomUser
        exclude = ('password',)
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'authentication_status')


class nationaluploadform(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['national_card_image']

class birthuploadform(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['birth_card_image']
class avataruploadform(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['avatar_image']