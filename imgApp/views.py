from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from django.conf import settings

# for boto3 
import boto3
import botocore
from botocore.exceptions import ClientError

# for filtering
from PIL import Image, ImageOps, ImageFilter

# for downloading portion
from wsgiref.util import FileWrapper
import mimetypes
from django.conf import settings

from django.contrib.staticfiles.views import serve

def fileExistedOnS3(bucketName, fileName):
    s3 = boto3.resource('s3')
    
    try:
        s3.Object(bucketName, fileName).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            # The object does not exist.
            return False
        else:
            # Something else has gone wrong.
            raise
    else:
        # The object does exist.
        return True

def download_image_from_S3(request, bucket_name, image_name):
    
    # if found image from S3, then let's it download
    
    s3_client = boto3.client('s3')

    image_found = fileExistedOnS3(bucket_name, image_name)
    print("Name of the image is {}".format(image_name)) 
    print("Value of image_found is {}".format(image_found))
    if image_found:
        # download image to root of media directory
        dest = settings.MEDIA_ROOT + "/images/" + image_name
        
        print("The destination is {}".format(dest))
        return serve(request, dest, insecure=True)
        #s3_client.download_file(bucket_name, image_name, dest)
        #response = HttpResponse(content_type='application/force-download') # mimetype is replaced by content_type for django 1.7
        #response['Content-Disposition'] = 'attachment; filename=%s' % dest.split("/")[-1]
        #response['X-Sendfile'] = smart_str(dest)
        # It's usually a good idea to set the 'Content-Length' header too.
        # You can also set any other required headers: Cache-Control, etc.
        #return response
        #with open(dest, "rb") as f:
            #print("Downloading " + dest)
            #return HttpResponse(f.read(), content_type="image/jpeg")
        #response = HttpResponse(content_type="image/png")
        #img = Image.open(dest)
        #img.save(response,'png')
        #return response 
        # get image
        #img = ImageModel.objects.get(name=image_name)
        # img = Image.open(dest)
        '''wrapper      = FileWrapper(open(dest))  # img.file returns full path to the image
        content_type = mimetypes.guess_type(dest.split("/")[-1])[0]  # Use mimetypes to get file type
        response     = HttpResponse(wrapper,content_type=content_type)  
        response['Content-Length']      = os.path.getsize(dest)    
        response['Content-Disposition'] = "attachment; filename=%s" %  dest.split("/")[-1]
        return response'''
    # if not, then dont let it download
    else:
        return redirect('imgNotFound')

def apply_filter(file_path, preset):
    
    im = Image.open(file_path)
    fileExt = file_path.split(".")[-1]

    if preset == 'none':
        print("No need for filter")
    else:
        ext = ''
        if preset == 'gray':
            im = ImageOps.grayscale(im)
            ext = 'gray'
        if preset == 'poster':
            im = ImageOps.posterize(im, 3)
            ext = 'poster'
        if preset == 'solar':
            im = ImageOps.solarize(im, threshold=80)
            ext = 'solar'
        im.save(file_path.split(".")[0] + "_" + ext + "." + fileExt)
    
        print("Filter was applied successfully")


def upload_to_s3(file_name, bucket, object_name):
   # Upload the file
    s3_client = boto3.client('s3')

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        print(e)
        return False
    return True

# Create your views here.
def image_view(request):

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        # since request.POST is a QueryDict
        # we must convert it to a normal dictionary data type
        # then we can access the field name from there

        print("The file name is: " + request.POST.dict()["name"])
        bucket = "4517-image-app"

        # since the upload_to function replaces white space with _ 
        # in the name
        # we must do the same here in order to find the image
        ext = request.POST.dict()["ext"]

        file_path = settings.MEDIA_ROOT + "/images/" + request.POST.dict()["name"].replace(" ", "_") + "." + ext 
        
        print(file_path)
        
        preset = request.POST.dict()["preset_gray_or_poster_or_solar_or_none"]

        if form.is_valid():
            form.save()

            # apply filter
            apply_filter(file_path, preset)

            # upload image to s3
            upload_to_s3(file_path, bucket, request.POST.dict()["name"].replace(" ", "_") + "_" + preset + "." + ext)
            return redirect('success')
    else:
        form = ImageForm()
    return render(request, 'submit.html', {'form' : form})

# Python program to view  
# for displaying images 
def display_images(request): 
  
    if request.method == 'GET': 
  
        # getting all the objects of hotel. 
        Images = ImageModel.objects.all()  
        return render(request, 'display_images.html', {'images': Images}) 

def download_images_view(request):

    if request.method == 'POST':
        
        # get images
        form = DownloadImageForm(request.POST, request.FILES)
        ext = request.POST.dict()["ext"]
        img_name = request.POST.dict()["name_To_Download"].replace(" ", "_")
        pretext = request.POST.dict()["preset_gray_or_poster_or_solar_or_none"]
        bucket = "4517-image-app"
        
        if form.is_valid():
            form.save()
            
            print("Downloading file from S3")

            download_image_from_S3(request, bucket, img_name + "_" + pretext + "." + ext)    
    else:
        form = DownloadImageForm()
    return render(request, 'download.html', {'form' : form})

def success(request):
    return HttpResponse('successfully uploaded')

def imgNotFound(request):
    return HttpResponse('Image Not Found. Please go back to the search image page.')
