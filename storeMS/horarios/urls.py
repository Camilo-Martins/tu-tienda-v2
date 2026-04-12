from django.urls import path
from .views import*

urlpatterns = [
    path('obtener-horario', ObtenerHorario.as_view()), 
    path('crear', CrearHorario.as_view()), 
    path('asignacion-personal/<int:id>', AsignarSemana.as_view()), 
    path('eliminacion-personal/<int:id>', DesasignarSemana.as_view()), 
]
