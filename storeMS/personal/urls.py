from django.urls import path
from .views import*

urlpatterns = [
    path('agregar', RegistroEmpleado.as_view()),
    path('obtener', ObtenerEmpleados.as_view()),
    path('obtener/lista', ObtenerEmpleadosActivos.as_view()),
    path('editar/<int:id>', EditarEmpleado.as_view()),
]
