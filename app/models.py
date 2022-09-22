from django.db import models

# It creates a class called Uso.
class Uso(models.Model):
    nombre = models.TextField()

    def __str__(self):
        return self.nombre

# It creates a class called Planta.
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

# It creates a class called Seccion.
class Seccion(models.Model):
    descripcion = models.TextField()

# It creates a class called Imagen.
class Imagen(models.Model):
    dato = models.TextField()
    tipo = models.CharField(max_length=256, help_text='The MIMEType of the file')
    planta = models.ForeignKey(Planta, related_name='Pimagenes', on_delete=models.CASCADE, null=True)
    seccion = models.ForeignKey(Seccion, related_name='Simagenes', on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.tipo
# It creates a class called Analiticos.
class Analiticos(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    