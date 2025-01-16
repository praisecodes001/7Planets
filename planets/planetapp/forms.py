from django import forms
from django.forms import ModelForm
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class PostForm(forms.ModelForm):
      class Meta:
              model = Post
              fields = '__all__'



class CreateUserForm(UserCreationForm):
       class Meta:
           model = User
           fields = ['username', 'email', 'password1', 'password2', ]
       
