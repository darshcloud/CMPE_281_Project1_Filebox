import os

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser, FormParser
from backendapp.filebox_s3_storage import FileStorage
from backendapp.models import Files
from datetime import datetime
import boto3


# Create your views here.
class RegisterView(APIView):
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


class UploadFileView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        # if request.user.is_authenticated():
        username = 'darshini'
        data = request.POST
        file_obj = request.FILES.get('file_data')
        file_description = data['file_description']
        # upload to S3
        directory_path_in_bucket = "filebox_files/{username}".format(username=username)
        file_path_in_bucket = '/'.join([directory_path_in_bucket, file_obj.name])
        file_storage = FileStorage()
        # options = {
        #     "Metadata": {
        #         "description": file_description,
        #         "created_time": str(datetime.now()),
        #         "updated_time": str(datetime.now())
        #     }
        # }
        # file_storage.object_parameters.update(options)
        file_details = Files(
            file_key=file_path_in_bucket,
            username=username,
            file_description=file_description,
        )
        file_details.save()
        if not file_storage.exists(file_path_in_bucket):  # avoid overwriting existing file
            file_storage.save(file_path_in_bucket, file_obj)
            file_url = file_storage.url(file_path_in_bucket)

            return Response({
                'result': 'success',
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


class ListFilesView(APIView):

    def get(self, request):
        username = 'darshini'
        files_data = {}
        files = Files.objects.filter(username=username)
        for file in files:
            files_data[file.file_key] = {
                'file_description': file.file_description,
                'created_time': file.created_time,
                'updated_time': file.updated_time
            }
        # file_storage = FileStorage()
        # directory_path_in_bucket = '/'.join(["filebox_files", username])
        # dirs, files = file_storage.listdir(directory_path_in_bucket)
        # s3_resource = boto3.resource("s3")
        # files_data = {}
        # for file in files:
        #     s3_obj = s3_resource.Object('filebox-company-primary', '/'.join([directory_path_in_bucket, file]))
        #     metadata = s3_obj.metadata
        #     files_data[file] = {
        #         'description': metadata.get('description'),
        #         'created_time': metadata.get('created_time'),
        #         'updated_time': metadata.get('updated_time')
        #     }
        return Response(files_data)


class DeleteFileView(APIView):

    def delete(self, request):
        file_storage = FileStorage()
        username = 'darshini'
        filename = request.data['filename']
        directory_path_in_bucket = "filebox_files/{username}".format(username=username)
        file_path_in_bucket = '/'.join([directory_path_in_bucket, filename])
        file_storage.delete(file_path_in_bucket)
        Files.objects.filter(file_key=file_path_in_bucket).delete()
        return Response({'result': 'success',
                         'message': 'File successfully deleted'})


class UpdateFileView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        username = 'darshini'
        data = request.POST
        file_obj = request.FILES.get('file_data') if "file_data" in request.FILES else None
        file_description = data['file_description']
        filename = data['filename']
        directory_path_in_bucket = "filebox_files/{username}".format(username=username)
        file_path_in_bucket = '/'.join([directory_path_in_bucket, filename])
        if file_obj:
            # upload to S3
            file_storage = FileStorage()
            # options = {
            #     "Metadata": {
            #         "description": file_description,
            #         "updated_time": str(datetime.now())
            #     }
            # }
            # file_storage.object_parameters.update(options)
            file_storage.save(file_path_in_bucket, file_obj)
        file_data = Files.objects.get(file_key=file_path_in_bucket)
        file_data.file_description = file_description
        file_data.updated_time = datetime.now()
        file_data.save()
        return Response({
            'result': 'Success',
            'message': 'File updated successfully'
        })
