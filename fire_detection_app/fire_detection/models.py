from django.db import models

# Create your models here.
class FileUpload(models.Model):
    video_file=models.FileField(upload_to='')
    image_file=models.ImageField(upload_to='')

  
