from django.urls import path
from .views import*

urlpatterns = [
    path('obtener/', ObtenerPublicidad.as_view()),
    path('obtener/vigentes', ObtenerPublicidadVigente.as_view()),
    path('agregar', AgregarPublicidad.as_view()),
    path('editar/<int:id>', EditarPublicidad.as_view())
   
]
