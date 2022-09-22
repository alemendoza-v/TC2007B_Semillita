from django.db import models

# Create your models here.
class Uso(models.Model):
    nombre = models.TextField()

    def __str__(self):
        return self.nombre

class Planta(models.Model):
    nombre_cientifico = models.TextField()
    nombre_tradicional = models.TextField()
    especie = models.TextField()
    origen = models.TextField()
    temporada = models.TextField()
    estatus = models.BooleanField(default=True, editable=True)
    descripcion = models.TextField()
    fertilizante = models.TextField()
    riego = models.TextField()
    iluminacion = models.TextField()

    usos = models.ManyToManyField(Uso)

class Seccion(models.Model):
    descripcion = models.TextField()

class Imagen(models.Model):
    dato = models.TextField()
    tipo = models.CharField(max_length=256, help_text='The MIMEType of the file')
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, null=True)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.tipo
class Analiticos(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    