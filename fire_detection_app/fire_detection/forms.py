from django import forms
from . models import FileUpload

class FileUploads(forms.ModelForm):
   class Meta:
      model=FileUpload
      fields='__all__'