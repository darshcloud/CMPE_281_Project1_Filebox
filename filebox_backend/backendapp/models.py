from django.db import models
from datetime import datetime


# Create your models here.
class Files(models.Model):
    file_key = models.CharField(max_length=255, primary_key=True)
    username = models.CharField(max_length=150, db_index=True)
    file_description = models.TextField()
    created_time = models.DateTimeField(default=datetime.now())
    updated_time = models.DateTimeField(default=datetime.now())
