from django.db import models
from django.db.models import Q

from .validators import normalize_phone


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "clientes_venta"
        ordering = ["nombre", "id"]
        verbose_name = "Cliente de venta"
        verbose_name_plural = "Clientes de venta"

    def save(self, *args, **kwargs):
        self.telefono = normalize_phone(self.telefono)
        self.nombre = self.nombre.strip()
        super().save(*args, **kwargs)

    @property
    def saldo_pendiente(self):
        from django.db.models import Sum

        total_fiado = self.ventas.filter(tipo=Venta.Tipo.FIADO).aggregate(
            total=Sum("total")
        )["total"] or 0
        total_abonado = Abono.objects.filter(
            venta__cliente=self, venta__tipo=Venta.Tipo.FIADO
        ).aggregate(total=Sum("monto"))["total"] or 0
        return max(total_fiado - total_abonado, 0)

    def __str__(self):
        return f"{self.nombre} ({self.telefono})"


class Venta(models.Model):
    class Tipo(models.TextChoices):
        CONTADO = "CONTADO", "Pagada"
        FIADO = "FIADO", "Fiada"

    tipo = models.CharField(max_length=10, choices=Tipo.choices, db_index=True)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="ventas",
    )
    total = models.PositiveBigIntegerField()
    fecha = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "ventas"
        ordering = ["-fecha", "-id"]

    def __str__(self):
        return f"Venta #{self.pk} ({self.get_tipo_display()})"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(
        "productos.Producto",
        on_delete=models.PROTECT,
        related_name="detalles_venta",
    )
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.PositiveBigIntegerField()

    class Meta:
        db_table = "ventas_detalle"
        constraints = [
            models.UniqueConstraint(
                fields=["venta", "producto"], name="venta_producto_unico"
            ),
            models.CheckConstraint(check=Q(cantidad__gt=0), name="detalle_cantidad_positiva"),
        ]

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario


class Abono(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.PROTECT, related_name="abonos")
    monto = models.PositiveBigIntegerField()
    fecha = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "ventas_abonos"
        ordering = ["-fecha", "-id"]
        constraints = [
            models.CheckConstraint(check=Q(monto__gt=0), name="abono_monto_positivo"),
        ]

    def __str__(self):
        return f"Abono de ${self.monto} a venta #{self.venta_id}"
