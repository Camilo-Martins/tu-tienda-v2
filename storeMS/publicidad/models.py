from django.db import models

# Create your models here.
class Publicidad(models.Model):
    
    nombre = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(blank=True, upload_to="publicidad/")
    nombre_autor = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table='publicidad'
        verbose_name='Publicidad'
        verbose_name_plural='Publicidad'