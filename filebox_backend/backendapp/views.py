import os

from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser, FormParser
from backendapp.filebox_s3_storage import FileStorage
from backendapp.models import Files
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


# Create your views here.
class RegisterUserView(APIView):
    def post(self, request):
        username = request.data['username']
        firstname = request.data['firstname']
        lastname = request.data['lastname']
        email = request.data['email']
        password = request.data['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        return Response({'result': 'success',
                         'message': 'User Registered Successfully'})


class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'is_staff': user.is_staff
        })


class FilesView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.user.username
        data = request.POST
        file_obj = request.FILES.get('file')
        file_description = data['file_description']
        # upload to S3
        directory_path_in_bucket = "filebox_files/{username}".format(username=username)
        file_path_in_bucket = '/'.join([directory_path_in_bucket, file_obj.name])
        file_storage = FileStorage()
        file_details = Files(
            file_key=file_path_in_bucket,
            file_name=file_obj.name,
            username=username,
            file_description=file_description
        )
        file_details.save()
        if not file_storage.exists(file_path_in_bucket):  # avoid overwriting existing file
            file_storage.save(file_path_in_bucket, file_obj)
            file_url = file_storage.url(file_path_in_bucket)

            return Response({
                'result': 'success',
                'message': 'File uploaded successfully',
                'fileUrl': file_url,
            })
        else:
            return Response({
                'message': 'Error: file {filename} already exists at {file_directory} in bucket {bucket_name}'.format(
                    filename=file_obj.name,
                    file_directory=directory_path_in_bucket,
                    bucket_name=file_storage.bucket_name
                ),
            }, status=400)

    def get(self, request):
        username = request.user.username
        files_data = {}
        if request.user.is_staff:
            files = Files.objects.all()
        else:
            files = Files.objects.filter(username=username)
        file_storage = FileStorage()
        user_dict = {}
        for file in files:
            if file.username not in user_dict:
                user = get_object_or_404(User, username=file.username)
                user_dict[file.username] = user
            files_data[file.file_key.split('/')[-1]] = {
                'file_username': file.username,
                'file_description': file.file_description,
                'created_time': file.created_time,
                'updated_time': file.updated_time,
                'file_url': file_storage.url(file.file_key),
                'first_name': user_dict[file.username].first_name,
                'last_name': user_dict[file.username].last_name
            }
        return Response(files_data)

    def delete(self, request):
        file_storage = FileStorage()
        username = request.user.username
        filename = request.data['filename']
        file_user = request.data['username']
        if request.user.is_staff:
            file_path_in_bucket = Files.objects.get(file_name=filename, username=file_user).file_key
        else:
            directory_path_in_bucket = "filebox_files/{username}".format(username=username)
            file_path_in_bucket = '/'.join([directory_path_in_bucket, filename])
        file_storage.delete(file_path_in_bucket)
        Files.objects.filter(file_key=file_path_in_bucket).delete()
        return Response({'result': 'success',
                         'message': 'File successfully deleted'})

    def put(self, request):
        username = request.user.username
        data = request.POST
        file_obj = request.FILES.get('file') if "file" in request.FILES else None
        file_description = data['file_description']
        filename = data['filename']
        directory_path_in_bucket = "filebox_files/{username}".format(username=username)
        file_path_in_bucket = '/'.join([directory_path_in_bucket, filename])
        if file_obj:
            file_storage = FileStorage()
            file_storage.save(file_path_in_bucket, file_obj)
        file_data = Files.objects.get(file_key=file_path_in_bucket)
        file_data.file_description = file_description
        file_data.updated_time = datetime.now()
        file_data.save()
        return Response({
            'result': 'Success',
            'message': 'File updated successfully'
        })
