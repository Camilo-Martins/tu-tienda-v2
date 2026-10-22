from django.db import models

# Create your models here.
class HorarioSemanal(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()  # lunes de la semana
    fecha_fin = models.DateField()     # sabado de la misma semana
    is_active = models.BooleanField(default=True)
   

    def __str__(self):
        return self.nombre

    class Meta:
        db_table='horario'
        verbose_name='Horario'
        verbose_name_plural='Horarios'