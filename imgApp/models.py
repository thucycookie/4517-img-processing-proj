from django.db import models

# Create your models here.

# Referenced this source to rename an image based on the user's input for
# the name field

import os

# rename the file as the input's name
# not the original name of the file
def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s" % (instance.name)
    return os.path.join('images', filename + "." + ext)


class ImageModel(models.Model): 
        name = models.CharField(max_length=50)
        preset_gray_or_poster_or_solar_or_none = models.CharField(max_length=50) 
        Main_Img = models.FileField(upload_to=content_file_name)
        ext = models.CharField(max_length=50)

class DownloadImageModel(models.Model):
        name_To_Download = models.CharField(max_length=50)
        preset_gray_or_poster_or_solar_or_none = models.CharField(max_length=50)
        ext = models.CharField(max_length=50)
