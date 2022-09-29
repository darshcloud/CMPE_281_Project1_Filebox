# forms to be defined here

from django import forms
from django.forms import PasswordInput


# code representation of the form

class LoginForm(forms.Form):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter the username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter the password'}))

    def clean_username(self):
        data = self.cleaned_data['username']
        return data

    def clean_password(self):
        data = self.cleaned_data['password']
        return data


class RegisterForm(forms.Form):
    firstname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'}))
    lastname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter the password'}))

    def clean_firstname(self):
        data = self.cleaned_data['firstname']
        return data

    def clean_lastname(self):
        data = self.cleaned_data['lastname']
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        return data

    def clean_password(self):
        data = self.cleaned_data['password']
        return data


class UploadFileForm(forms.Form):
    file = forms.FileField()
    file_description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter file description'}))

    def clean_file(self):
        data = self.cleaned_data['file']
        return data

    def clean_file_description(self):
        data = self.cleaned_data['file_description']
        return data


class UpdateFileForm(forms.Form):
    file = forms.FileField()
    filename = forms.CharField(disabled=True)
    file_description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter file description'}))
    file_uploaded_time = forms.DateTimeField(disabled=True)
    file_updated_time = forms.DateTimeField(disabled=True)

    def clean_file(self):
        data = self.cleaned_data['file']
        return data

    def clean_file_description(self):
        data = self.cleaned_data['file_description']
        return data

    def clean_file_uploaded_time(self):
        data = self.cleaned_data['file_uploaded_time']
        return data

    def clean_file_updated_time(self):
        data = self.cleaned_data['file_updated_time']
        return data
