from django import forms
from django.forms import ModelForm
from job_search.models import User
from job_search.models import Employers
from django.contrib.auth.forms import UserCreationForm

class UserForm(ModelForm):
    class Meta:
        model = User
        fields=[
            'name',           
            'email',
            'phone',
            'bio',
            'organization',
            'location',
            'about',
            'avatar',
            'logo',
            'video',           
        ]

# class UserRegistrationForm(UserCreationForm):
#     class Meta:
#         model = Employers
#         fields = ['name', 'organization', 'email', 'password2']
#         widgets = {
#             'password': forms.PasswordInput(),
#         }

# class UserLoginForm(forms.Form):
#     email = forms.EmailField(label='Email')
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)
