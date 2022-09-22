import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from fileboxapp.forms import LoginForm
from fileboxapp.forms import RegisterForm
from fileboxapp.forms import UploadFileForm
from fileboxapp.forms import UpdateFileForm


# Create your views here.
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.post)
        if form.is_valid():
            # here you need to encrypt the password call rest api into login service and get a token
            HttpResponseRedirect(reverse('home'))
    else:
        form = LoginForm(initial={'username': '', 'password': ''})
    context = {'form': form}
    return render(request, 'login.html', context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.post)
        if form.is_valid():
            # here you need to encrypt the password call rest api into login service and get a token
            HttpResponseRedirect(reverse('login'))
    else:
        form = RegisterForm(initial={'firstname': '', 'lastname': '', 'email': '', 'password': ''})
    context = {'form_key': form}
    return render(request, 'register.html', context)


def home(request):
    if request.method == 'POST':
        form = UploadFileForm(request.post)
        if form.is_valid():
            # upload to s3 bucket - call backend service
            HttpResponseRedirect(reverse('home'))
    else:
        # fetch the uploaded files data from backend server
        files_data = {}
        form = UploadFileForm(initial={'file': '', 'file_description': ''})
        context = {'form_key': form, 'files_data': files_data}
        return render(request, 'home.html', context)


def update(request):
    if request.method == 'POST':
        form = UpdateFileForm(request.post)
        if form.is_valid():
            # update the file to s3 - call backend service
            HttpResponseRedirect(reverse('home'))
    else:
        # fetch the data from the request and populate it to form
        file_data = {
            "file": "abc/def",
            "file_desc": "test_file",
            "file_upload_time": datetime.datetime.now(),
            "file_update_time": datetime.datetime.now()
        }
        form = UpdateFileForm(initial={
            'file': file_data['file'],
            'file_description': file_data['file_desc'],
            'file_uploaded_time': file_data['file_upload_time'],
            'file_updated_time': file_data['file_update_time']})
        context = {"form_key": form}
        return render(request, 'update.html', context)