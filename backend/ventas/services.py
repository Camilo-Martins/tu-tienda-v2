from collections import defaultdict

from django.db import IntegrityError, transaction
from django.db.models import Sum

from productos.models import Producto

from .models import Abono, Cliente, DetalleVenta, Venta
from .validators import normalize_phone


class VentaError(Exception):
    status_code = 400


class StockInsuficienteError(VentaError):
    status_code = 409


class PrecioActualizadoError(VentaError):
    status_code = 409


def _get_or_create_cliente(nombre, telefono):
    telefono = normalize_phone(telefono)
    cliente = Cliente.objects.select_for_update().filter(telefono=telefono).first()
    if cliente:
        return cliente

    try:
        # The savepoint lets a concurrent request win the unique-phone race safely.
        with transaction.atomic():
            return Cliente.objects.create(nombre=nombre.strip(), telefono=telefono)
    except IntegrityError:
        return Cliente.objects.select_for_update().get(telefono=telefono)


@transaction.atomic
def crear_venta(*, tipo, items, cliente_data=None):
    if not items:
        raise VentaError("Agregue al menos un producto a la venta.")

    if tipo == Venta.Tipo.FIADO:
        if not cliente_data:
            raise VentaError("Para registrar una venta fiada debe indicar el cliente.")
        cliente = _get_or_create_cliente(
            cliente_data["nombre"], cliente_data["telefono"]
        )
    else:
        if cliente_data:
            raise VentaError("Las ventas pagadas no necesitan datos de cliente.")
        cliente = None

    cantidades = defaultdict(int)
    precios_esperados = {}
    for item in items:
        producto_id = item["producto_id"]
        precio = item["precio_esperado"]
        if producto_id in precios_esperados and precios_esperados[producto_id] != precio:
            raise VentaError("El carrito tiene precios inconsistentes para un producto.")
        precios_esperados[producto_id] = precio
        cantidades[producto_id] += item["cantidad"]

    productos = {
        producto.pk: producto
        for producto in Producto.objects.select_for_update()
        .filter(pk__in=sorted(cantidades))
        .order_by("pk")
    }

    if len(productos) != len(cantidades):
        raise VentaError("Uno o más productos ya no existen.")

    total = 0
    for producto_id, cantidad in cantidades.items():
        producto = productos[producto_id]
        if not producto.is_active:
            raise VentaError(f"{producto.nombre_producto} ya no está disponible.")
        stock = producto.stock_actual or 0
        if stock <= 0:
            raise StockInsuficienteError(
                f"{producto.nombre_producto} no tiene stock disponible."
            )
        if cantidad > stock:
            raise StockInsuficienteError(
                f"Stock insuficiente para {producto.nombre_producto}: "
                f"solicitado {cantidad}, disponible {stock}."
            )
        if producto.precio is None:
            raise VentaError(f"{producto.nombre_producto} no tiene un precio definido.")
        if producto.precio != precios_esperados[producto_id]:
            raise PrecioActualizadoError(
                f"El precio de {producto.nombre_producto} cambió. "
                "Revisa el carrito antes de confirmar."
            )
        total += cantidad * producto.precio

    venta = Venta.objects.create(tipo=tipo, cliente=cliente, total=total)
    detalles = []
    for producto_id, cantidad in cantidades.items():
        producto = productos[producto_id]
        detalles.append(
            DetalleVenta(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio,
            )
        )
        producto.stock_actual -= cantidad
        producto.save(update_fields=["stock_actual"])

    DetalleVenta.objects.bulk_create(detalles)
    return venta


@transaction.atomic
def registrar_abono(*, cliente_id, venta_id, monto):
    cliente = Cliente.objects.select_for_update().filter(pk=cliente_id).first()
    if not cliente:
        raise VentaError("No se encontró el cliente.")

    venta = (
        Venta.objects.select_for_update()
        .filter(pk=venta_id, cliente=cliente, tipo=Venta.Tipo.FIADO)
        .first()
    )
    if not venta:
        raise VentaError("La venta fiada no pertenece a este cliente.")

    abonado = venta.abonos.aggregate(total=Sum("monto"))["total"] or 0
    saldo = venta.total - abonado
    if saldo <= 0:
        raise VentaError("Esta venta ya está saldada.")
    if monto > saldo:
        raise VentaError(f"El abono no puede superar el saldo pendiente de ${saldo}.")

    return Abono.objects.create(venta=venta, monto=monto)


def obtener_clientes(*, telefono=None, busqueda=None, estado=None):
    from django.db.models import BigIntegerField, F, OuterRef, Subquery, Value
    from django.db.models.functions import Coalesce

    fiadas = (
        Venta.objects.filter(cliente_id=OuterRef("pk"), tipo=Venta.Tipo.FIADO)
        .order_by()
        .values("cliente_id")
        .annotate(total=Sum("total"))
        .values("total")[:1]
    )
    abonos = (
        Abono.objects.filter(venta__cliente_id=OuterRef("pk"), venta__tipo=Venta.Tipo.FIADO)
        .order_by()
        .values("venta__cliente_id")
        .annotate(total=Sum("monto"))
        .values("total")[:1]
    )

    clientes = Cliente.objects.annotate(
        _total_fiado=Coalesce(
            Subquery(fiadas, output_field=BigIntegerField()),
            Value(0),
            output_field=BigIntegerField(),
        ),
        _total_abonado=Coalesce(
            Subquery(abonos, output_field=BigIntegerField()),
            Value(0),
            output_field=BigIntegerField(),
        ),
    ).annotate(_saldo_pendiente=F("_total_fiado") - F("_total_abonado"))

    if telefono:
        clientes = clientes.filter(telefono=normalize_phone(telefono))
    if busqueda:
        clientes = clientes.filter(nombre__icontains=busqueda)
    if estado == "deuda":
        clientes = clientes.filter(_saldo_pendiente__gt=0)
    elif estado == "sin_deudas":
        clientes = clientes.filter(_saldo_pendiente__lte=0)
    return clientes.order_by("nombre", "id")

