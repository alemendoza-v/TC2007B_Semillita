from django.forms import ModelForm, ClearableFileInput,FileField
from models import Imagen

class ImagenForm(ModelForm):
    class Meta:
        model = Imagen
        exclude = ['id']
        dato = FileField()
