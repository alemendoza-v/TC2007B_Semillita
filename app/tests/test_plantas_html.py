from django.test import TestCase

from django.core.files.uploadedfile import SimpleUploadedFile

from app.models import Planta, Uso, Imagen

class PlantaTestHTMLView(TestCase):
    def setUp(self):
        self.uri = '/plantas/'

    def test_scan(self):
        planta = Planta.objects.create(
            nombre_cientifico = 'Planta de prueba',
            nombre_tradicional = 'Plantita',
            especie = 'Arbusto',
            origen = 'Mexico',
            temporada = 'Invierno',
            descripcion = 'Buena planta',
            fertilizante = 'No necesita',
            riego = '100 ml diarios',
            iluminacion = 'Sombra parcial',
        )
        planta.usos.add(Uso.objects.create(nombre='Medicinal'))
        planta.save()
        image = SimpleUploadedFile(name='test_image.jpg', content=b"file_content", content_type='image/jpeg')
        Imagen.objects.create(
            dato=image,
            tipo='image/jpeg',
            planta_id=planta.id
        )
        response = self.client.get(self.uri + str(planta.id) + "/")
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(response.status_code))
        self.assertTemplateUsed(response, 'planta_detail.html')
        print('Planta HTML View test passed')