from django.forms import ModelForm
from .models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2','is_employer','is_employee']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields=[
            'name',           
            'email',
            'phone',
            'skills',
            'bio',
            'education',
            'experience',
            'location',
            'avatar',
            'cv',
            'video', 

                      
        ]

class ComplaintUser(ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'complaints'
        ]
        

