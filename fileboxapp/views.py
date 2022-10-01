import datetime

from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from fileboxapp.forms import LoginForm
from fileboxapp.forms import RegisterForm
from fileboxapp.forms import UploadFileForm
from fileboxapp.forms import UpdateFileForm
from filebox_frontend.settings import FILEBOX_BACKEND_SERVER
import requests
from django.contrib import messages

FILES_URL = FILEBOX_BACKEND_SERVER + "/api/files/"
MAX_FILE_SIZE = 10*1024*1024


# Create your views here.
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = {
                "username": form.cleaned_data['username'],
                "password": form.cleaned_data['password']
            }
            login_url = FILEBOX_BACKEND_SERVER + "/user/authorize/"
            login_response = requests.post(url=login_url, data=data)
            json_response = login_response.json()
            if login_response.status_code != 200:
                for key, value in json_response.items():
                    messages.error(request, '.'.join(value))
                return HttpResponseRedirect(reverse('login'))
            login_token = json_response.get('token')
            is_staff = json_response.get('is_staff')
            redirect_response = HttpResponseRedirect(reverse('home'))
            redirect_response.set_cookie('token', login_token)
            redirect_response.set_cookie('username', form.cleaned_data['username'])
            redirect_response.set_cookie('isStaff', is_staff)
            return redirect_response
    else:
        form = LoginForm(initial={'username': '', 'password': ''})
    context = {'form_key': form}
    return render(request, 'login.html', context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = {
                "username": form.cleaned_data['email'],
                "password": form.cleaned_data['password'],
                "firstname": form.cleaned_data['firstname'],
                "lastname": form.cleaned_data['lastname'],
                "email": form.cleaned_data['email']
            }
            register_url = FILEBOX_BACKEND_SERVER + "/user/register/"
            register_response = requests.post(url=register_url, data=data)
            register_response.raise_for_status()
            return HttpResponseRedirect(reverse('login'))
    else:
        form = RegisterForm(initial={'firstname': '', 'lastname': '', 'email': '', 'password': ''})
    context = {'form_key': form}
    return render(request, 'register.html', context)


def home(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            data = {
                "file_description": form.cleaned_data['file_description']
            }

            file_size = request.FILES['file'].size
            if file_size > MAX_FILE_SIZE:
                messages.error(request, 'Please Upload a File less than 10MB')
                return HttpResponseRedirect(reverse('home'))

            headers = {
                "Authorization": "Token " + request.COOKIES['token']
            }
            upload_response = requests.post(url=FILES_URL, headers=headers, data=data, files=request.FILES)
            upload_response.raise_for_status()
            return HttpResponseRedirect(reverse('home'))
    else:
        headers = {
            "Authorization": "Token " + request.COOKIES['token']
        }
        files_get_response = requests.get(url=FILES_URL, headers=headers)
        files_data = files_get_response.json()
        form = UploadFileForm(initial={'file': '', 'file_description': ''})
        context = {'form_key': form, 'files_data': files_data}
        return render(request, 'home.html', context)


def update(request, file_name, file_desc, uploaded_time, updated_time):
    if request.method == 'POST':
        form = UpdateFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = request.FILES.get('file', None)
            data = {
                "filename": file_name,
                "file_description": form.cleaned_data['file_description']
            }
            if file_obj:
                file_size = file_obj.size
                if file_size > MAX_FILE_SIZE:
                    messages.error(request, 'Please Upload a File less than 10MB')
                    return HttpResponseRedirect(reverse('home'))
                if file_obj.name != file_name:
                    messages.error(request, 'Please Update a File with name {}'.format(file_name))
                    return HttpResponseRedirect(reverse('home'))

            headers = {
                "Authorization": "Token " + request.COOKIES['token']
            }
            files_get_response = requests.put(url=FILES_URL, headers=headers, data=data, files=request.FILES)
            files_get_response.raise_for_status()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = UpdateFileForm(initial={
            'file': '',
            'file_description': file_desc})
        file_data = {
            'filename': file_name,
            'file_uploaded_time': uploaded_time,
            'file_updated_time': updated_time}
        context = {"form_key": form, "file_data": file_data}
        return render(request, 'update.html', context)


def delete(request, file_name, file_username):
    if request.method == 'GET':
        data = {
            "filename": file_name,
            "username": file_username
        }
        headers = {
            "Authorization": "Token " + request.COOKIES['token']
        }
        delete_response = requests.delete(url=FILES_URL, headers=headers, data=data)
        delete_response.raise_for_status()
        return HttpResponseRedirect(reverse('home'))


def logout_user(request):
    logout(request)
    logout_response = HttpResponseRedirect(reverse('login'))
    logout_response.set_cookie('token', max_age=0)
    logout_response.set_cookie('username', max_age=0)
    logout_response.set_cookie('isStaff', max_age=0)
    return logout_response
