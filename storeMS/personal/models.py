from django.db import models

class Persona(models.Model):
 
    nombre_completo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    pago_diario = models.IntegerField(
        help_text="Monto acordado por día trabajado",
        default=0
    )
    rut = models.CharField(max_length=12, blank=True, null=True, default=999999)
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Referencia de cuándo comenzaron a trabajar juntos"
    )
   
    def __str__(self):
        return self.nombre_completo
    
    class Meta:
        db_table='personal'
        verbose_name='Personal'
        verbose_name_plural='Personal'
        