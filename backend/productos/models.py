from django.db import models
from proveedores.models import Proveedor

# Create your models here.
class Producto(models.Model):
    nombre_producto = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.PositiveIntegerField(blank=True, null=True, default=0)
    categoria = models.TextField(blank=True, null=True, default="Sin categoria")
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="productos"
    )
    stock_actual = models.PositiveIntegerField(blank=True, null=True, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_producto
    
    class Meta:
        db_table='productos'
        verbose_name='Productos'
        verbose_name_plural='Productos'