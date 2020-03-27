# forms.py 
from django import forms 
from .models import *
  
class ImageForm(forms.ModelForm): 
    class Meta:
        model = ImageModel
        fields = ['name', 'preset_gray_or_edge_or_blur_or_none', 'Main_Img', 'ext']

class DownloadImageForm(forms.ModelForm):
    class Meta:
        model = DownloadImageModel
        fields = ['name_To_Download', 'preset_gray_or_edge_or_blur_or_none', 'ext']
