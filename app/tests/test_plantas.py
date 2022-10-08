from rest_framework.test import APITestCase

from django.core.files.uploadedfile import SimpleUploadedFile

from app.models import Planta, Uso, Imagen

from django.contrib.auth.models import User

import json
import os
class TestPlantaViewSet(APITestCase):
    def setUp(self):
        # GIVEN
        self.user = User.objects.create_user(
            username='Goldie',
            password='testing1928',
            email=os.getenv('EMAIL_USER'),
        )
        self.user.save()
        # Plant view URI
        self.uri = '/api/plantas/'
        # Getting token
        self.data = {
            'username': 'Goldie',
            'password': 'testing1928',
        }
        self.data = json.dumps(self.data)
        self.token = self.client.post('/api/token/', self.data, content_type="application/json")
        self.token = json.loads(self.token.content)['access']

    def test_list(self):
        # WHEN
        request = self.client.get(self.uri, HTTP_AUTHORIZATION="Bearer " + self.token)
        # THEN
        self.assertEqual(request.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(request.status_code))
        print("Planta list test passed")

    def test_create_01(self):
        # GIVEN
        Uso.objects.create(nombre='Medicinal')
        data = {
            'nombre_cientifico': 'Planta de prueba',
            'nombre_tradicional': 'Plantita',
            'especie': 'Arbusto',
            'origen': 'Mexico',
            'temporada': 'Invierno',
            'descripcion': 'Buena planta',
            'fertilizante': 'No necesita',
            'riego': '100 ml diarios',
            'iluminacion': 'Sombra parcial',
            'usos': ['1'],
        }
        # WHEN
        request = self.client.post(self.uri, data, HTTP_AUTHORIZATION="Bearer " + self.token)
        # THEN
        self.assertEqual(request.status_code, 201, 'Expected Response Code 201, received {0} instead.'.format(request.status_code))
        print("Planta create test 01 passed")

    def test_create_02(self):
        # GIVEN
        Uso.objects.create(nombre='Medicinal')
        data = {
            'nombre_cientifico': 'Planta de prueba',
            'nombre_tradicional': 'Plantita',
            'especie': 'Arbusto',
            'origen': 'Mexico',
            'temporada': 'Invierno',
            'descripcion': 'Buena planta',
            'usos': ['1'],
        }
        # WHEN
        request = self.client.post(self.uri, data, HTTP_AUTHORIZATION="Bearer " + self.token)
        # THEN
        self.assertEqual(request.status_code, 400, 'Expected Response Code 400, received {0} instead.'.format(request.status_code))
        print("Planta create test 02 passed")

    def test_retrieve_01(self):
        # GIVEN
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
        # WHEN
        request = self.client.get(self.uri + str(planta.id) + '/', HTTP_AUTHORIZATION="Bearer " + self.token)
        # THEN
        self.assertEqual(request.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(request.status_code))
        print("Planta retrieve test 01 passed")    

    def test_retrieve_02(self):
        # GIVEN
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
        # WHEN
        planta.usos.add(Uso.objects.create(nombre='Medicinal'))
        request = self.client.get(self.uri + str(planta.id + 10) + '/', HTTP_AUTHORIZATION="Bearer " + self.token)
        # THEN
        self.assertEqual(request.status_code, 400, 'Expected Response Code 400, received {0} instead.'.format(request.status_code))
        print("Planta retrieve test 02 passed")

    def test_delete_01(self):
        # GIVEN
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
        image = SimpleUploadedFile('naranjo.jpg', content=b'file_content', content_type='image/jpg')
        Imagen.objects.create(
            dato = image,
            tipo = 'image/jpg',
            planta_id = planta.id,
        )
        # WHEN
        request = self.client.delete(self.uri + str(planta.id) + '/', HTTP_AUTHORIZATION="Bearer " + self.token)
        # THEN
        self.assertEqual(request.status_code, 204, 'Expected Response Code 204, received {0} instead.'.format(request.status_code))
        print("Planta delete test 01 passed")

    def test_delete_02(self):
        # GIVEN
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
        image = SimpleUploadedFile('naranjo.jpg', content=b'file_content', content_type='image/jpg')
        Imagen.objects.create(
            dato = image,
            tipo = 'image/jpg',
            planta_id = planta.id,
        )
        # WHEN
        request = self.client.delete(self.uri + str(planta.id + 10) + '/', HTTP_AUTHORIZATION="Bearer " + self.token)
        # THEN
        self.assertEqual(request.status_code, 400, 'Expected Response Code 400, received {0} instead.'.format(request.status_code))
        print("Planta delete test 02 passed")
    
    def test_update_01(self):
        # GIVEN
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
        image = SimpleUploadedFile('naranjo.jpg', content=b'file_content', content_type='image/jpg')
        planta.Pimagenes.add(Imagen.objects.create(
            dato = image,
            tipo = 'image/jpg',
            planta_id = planta.id,
        ))
        Uso.objects.create(nombre='Sombra')
        data = {
            'id' : planta.id,
            'nombre_cientifico': 'Planta modificada',
            'nombre_tradicional': 'Plantota',
            'especie': 'Arbol',
            'origen': 'Paris',
            'temporada': 'Otoño',
            'descripcion': 'Buenisima planta',
            'fertilizante': 'No es necesario',
            'riego': '3 litros diarios',
            'iluminacion': 'Sol directo',
            'usos': ['2'],
        }
        # WHEN
        request = self.client.put(self.uri + str(planta.id) + "/", data, HTTP_AUTHORIZATION="Bearer " + self.token)
        # THEN
        self.assertEqual(request.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(request.status_code))
        print("Planta update test 01 passed")

    def test_update_02(self):
        # GIVEN
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
        image = SimpleUploadedFile('naranjo.jpg', content=b'file_content', content_type='image/jpg')
        planta.Pimagenes.add(Imagen.objects.create(
            dato = image,
            tipo = 'image/jpg',
            planta_id = planta.id,
        ))
        Uso.objects.create(nombre='Sombra')
        data = {
            'id' : planta.id,
            'nombre_cientifico': 'Planta modificada',
            'nombre_tradicional': 'Plantota',
            'especie': 'Arbol',
            'origen': 'Paris',
            'temporada': 'Otoño',
            'descripcion': 'Buenisima planta',
            'fertilizante': 'No es necesario',
            'riego': '3 litros diarios',
            'iluminacion': 'Sol directo',
            'usos': ['2'],
        }
        # WHEN
        request = self.client.put(self.uri + str(planta.id + 10) + "/", data, HTTP_AUTHORIZATION="Bearer " + self.token)
        # THEN
        self.assertEqual(request.status_code, 400, 'Expected Response Code 400, received {0} instead.'.format(request.status_code))
        print("Planta update test 02 passed")
    
    def test_update_03(self):
        # GIVEN
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
        image = SimpleUploadedFile('naranjo.jpg', content=b'file_content', content_type='image/jpg')
        planta.Pimagenes.add(Imagen.objects.create(
            dato = image,
            tipo = 'image/jpg',
            planta_id = planta.id,
        ))
        Uso.objects.create(nombre='Sombra')
        data = {
            'id' : planta.id,
            'nombre_cientifico': 'Planta modificada',
            'nombre_tradicional': 'Plantota',
            'especie': 'Arbol',
            'origen': 'Paris',
            'temporada': 'Otoño',
            'descripcion': 'Buenisima planta',
            'usos': ['2'],
        }
        # WHEN
        request = self.client.put(self.uri + str(planta.id + 10) + "/", data, HTTP_AUTHORIZATION="Bearer " + self.token)
        # THEN
        self.assertEqual(request.status_code, 400, 'Expected Response Code 400, received {0} instead.'.format(request.status_code))
        print("Planta update test 03 passed")