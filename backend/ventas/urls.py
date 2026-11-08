from django.urls import path

from .views import (
    AbonosClienteView,
    ClienteComprasView,
    ClienteDetalleView,
    ClientesView,
    VentaDetalleView,
    VentasView,
)

urlpatterns = [
    path("", VentasView.as_view(), name="ventas-list-create"),
    path("clientes/", ClientesView.as_view(), name="clientes-list-create"),
    path("clientes/<int:cliente_id>/", ClienteDetalleView.as_view(), name="cliente-detail"),
    path("clientes/<int:cliente_id>/compras/", ClienteComprasView.as_view(), name="cliente-compras"),
    path("clientes/<int:cliente_id>/abonos/", AbonosClienteView.as_view(), name="cliente-abonos"),
    path("<int:venta_id>/", VentaDetalleView.as_view(), name="venta-detail"),
]
