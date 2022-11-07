from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfileModel


class UserRegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    firstname = forms.CharField(required=False, label='First name', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    lastname = forms.CharField(required=False, label='Last name', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    birth_date = forms.DateField(required=False, label='Birth Date', widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date'}))
    photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user:
            raise ValidationError('This email already exists')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if user:
            raise ValidationError('This username already exists')
        return username

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("confirm_password")
        if p1 and p2 and p1 != p2:
            raise ValidationError('Password and Confirm Password must match')


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class EditProfileForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    firstname = forms.CharField(required=False, label='First name',
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastname = forms.CharField(required=False, label='Last name',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    birth_date = forms.DateField(required=False, label='Birth Date',
                                 widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))

