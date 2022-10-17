from django.forms import ModelForm
from .models import User

class FileUploadForm(ModelForm):
    class Meta:
        model = User
        fields = ['imgfile',]