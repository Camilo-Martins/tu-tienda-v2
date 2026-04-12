from django.db import models


# Create your models here.
class Proveedor(models.Model):

    nombre_completo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=False, null=False)
    email = models.EmailField(max_length=50, blank=False, null=False, default="example@example.cl")
    rut = models.CharField(max_length=20, blank=False, null=False)
    nombre_empresa = models.CharField(max_length=150, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_completo
    
    class Meta:
        db_table='proveedores'
        verbose_name='Proveedores'
        verbose_name_plural='Proveedores'