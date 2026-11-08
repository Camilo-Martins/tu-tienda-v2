from django.contrib import admin

from .models import Abono, Cliente, DetalleVenta, Venta


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0
    readonly_fields = ("producto", "cantidad", "precio_unitario")


class AbonoInline(admin.TabularInline):
    model = Abono
    extra = 0
    readonly_fields = ("monto", "fecha")


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ("id", "tipo", "cliente", "total", "fecha")
    list_filter = ("tipo", "fecha")
    search_fields = ("cliente__nombre", "cliente__telefono")
    readonly_fields = ("tipo", "cliente", "total", "fecha")
    inlines = (DetalleVentaInline, AbonoInline)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "telefono", "created_at")
    search_fields = ("nombre", "telefono")
