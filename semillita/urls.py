"""semillita URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from app import views

# Creating a router object that will be used to register the viewsets.
router = routers.DefaultRouter()
# Registering the viewsets with the router.
router.register(r'plantas', views.PlantaViewSet, basename='plantas')
router.register(r'imagenes', views.ImagenViewSet, basename='imagenes')
router.register(r'analiticos', views.AnaliticosViewSet, basename='analiticos')
router.register(r'usos', views.UsosViewSet, basename='usos')

urlpatterns = [
    # The default admin page.
    path('admin/', admin.site.urls),
    # Including the urls from the router object.
    path('api/', include(router.urls)),
    # The default login page for the API.
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # A custom login view.
    path('api/users/', views.UserLogInView.as_view()),
    path('api/qr/', views.CreateQR.as_view()),
    path('plantas/<int:pk>/', views.PlantaDetailView.as_view(), name='planta_detail'),
    path('api/planta/<str:nombre_tradicional>/', views.PlantaGetView.as_view()),
]
