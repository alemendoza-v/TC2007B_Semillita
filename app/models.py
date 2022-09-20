from django.db import models

# Create your models here.
class Uso(models.Model):
    nombre = models.TextField()

class Planta(models.Model):
    nombre_cientifico = models.CharField(max_length=64)
    nombre_tradicional = models.CharField(max_length=32)
    especie = models.CharField(max_length=16)
    origen = models.CharField(max_length=32)
    temporada = models.CharField(max_length=24)
    estatus = models.BooleanField(default=True)
    descripcion = models.TextField()
    fertilizante = models.TextField()
    riego = models.TextField()
    iluminacion = models.TextField()

    usos = models.ManyToManyField(Uso)

class Seccion(models.Model):
    descripcion = models.TextField()

class Imagen(models.Model):
    dato = models.BinaryField(editable=True)
    tipo = models.CharField(max_length=256, help_text='The MIMEType of the file')
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, null=True)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, null=True)

class Analiticos(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    