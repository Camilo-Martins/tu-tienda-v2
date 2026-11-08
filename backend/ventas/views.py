from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Abono, Cliente, Venta
from .serializers import (
    AbonoSerializer,
    ClienteEditarSerializer,
    ClienteEntradaSerializer,
    ClienteSerializer,
    CrearAbonoSerializer,
    CrearVentaSerializer,
    VentaSerializer,
)
from .services import (
    VentaError,
    crear_venta,
    obtener_clientes,
    registrar_abono,
)


def _error_response(error, default_status=status.HTTP_400_BAD_REQUEST):
    return Response(
        {"estado": "error", "msg": str(error)},
        status=getattr(error, "status_code", default_status),
    )


def _ventas_queryset():
    return Venta.objects.select_related("cliente").prefetch_related(
        "items__producto", "abonos"
    )


class VentasView(APIView):
    def get(self, request):
        ventas = _ventas_queryset()
        cliente_id = request.query_params.get("cliente_id")
        tipo = request.query_params.get("tipo")
        desde = request.query_params.get("desde")
        hasta = request.query_params.get("hasta")
        orden = request.query_params.get("orden", "desc")

        if cliente_id:
            if not cliente_id.isdigit():
                return _error_response("cliente_id debe ser un número.")
            ventas = ventas.filter(cliente_id=int(cliente_id))
        if tipo:
            if tipo not in Venta.Tipo.values:
                return _error_response("tipo debe ser CONTADO o FIADO.")
            ventas = ventas.filter(tipo=tipo)
        if desde:
            parsed = parse_date(desde)
            if not parsed:
                return _error_response("desde debe tener formato AAAA-MM-DD.")
            ventas = ventas.filter(fecha__date__gte=parsed)
        if hasta:
            parsed = parse_date(hasta)
            if not parsed:
                return _error_response("hasta debe tener formato AAAA-MM-DD.")
            ventas = ventas.filter(fecha__date__lte=parsed)
        if desde and hasta:
            desde_date, hasta_date = parse_date(desde), parse_date(hasta)
            if desde_date and hasta_date and desde_date > hasta_date:
                return _error_response("desde no puede ser posterior a hasta.")
        if orden not in ("asc", "desc"):
            return _error_response("orden debe ser asc o desc.")

        direction = "" if orden == "asc" else "-"
        ventas = ventas.order_by(f"{direction}fecha", f"{direction}id")
        return Response({"estado": "ok", "data": VentaSerializer(ventas, many=True).data})

    def post(self, request):
        entrada = CrearVentaSerializer(data=request.data)
        if not entrada.is_valid():
            return Response(
                {"estado": "error", "msg": "Error de validación", "errors": entrada.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            venta = crear_venta(
                tipo=entrada.validated_data["tipo"],
                items=entrada.validated_data["items"],
                cliente_data=entrada.validated_data.get("cliente"),
            )
        except VentaError as error:
            return _error_response(error)
        venta = _ventas_queryset().get(pk=venta.pk)
        return Response(
            {"estado": "ok", "data": VentaSerializer(venta).data},
            status=status.HTTP_201_CREATED,
        )


class VentaDetalleView(APIView):
    def get(self, request, venta_id):
        venta = get_object_or_404(_ventas_queryset(), pk=venta_id)
        return Response({"estado": "ok", "data": VentaSerializer(venta).data})


class ClientesView(APIView):
    def get(self, request):
        estado = request.query_params.get("estado")
        if estado and estado not in ("deuda", "sin_deudas"):
            return _error_response("estado debe ser deuda o sin_deudas.")
        try:
            clientes = obtener_clientes(
                telefono=request.query_params.get("telefono"),
                busqueda=request.query_params.get("busqueda"),
                estado=estado,
            )
        except ValidationError as error:
            return Response(
                {"estado": "error", "msg": "Teléfono inválido", "errors": error.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"estado": "ok", "data": ClienteSerializer(clientes, many=True).data})

    def post(self, request):
        entrada = ClienteEntradaSerializer(data=request.data)
        if not entrada.is_valid():
            return Response(
                {"estado": "error", "msg": "Error de validación", "errors": entrada.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        telefono = entrada.validated_data["telefono"]
        cliente = Cliente.objects.filter(telefono=telefono).first()
        if cliente:
            return _error_response("Ese teléfono ya está asociado a un cliente.", status.HTTP_409_CONFLICT)
        try:
            with transaction.atomic():
                cliente = Cliente.objects.create(**entrada.validated_data)
        except IntegrityError:
            return _error_response(
                "Ese teléfono ya está asociado a un cliente.", status.HTTP_409_CONFLICT
            )
        cliente = obtener_clientes(telefono=cliente.telefono).get()
        return Response(
            {"estado": "ok", "data": ClienteSerializer(cliente).data},
            status=status.HTTP_201_CREATED,
        )


class ClienteDetalleView(APIView):
    def get(self, request, cliente_id):
        cliente = get_object_or_404(obtener_clientes(), pk=cliente_id)
        return Response({"estado": "ok", "data": ClienteSerializer(cliente).data})

    def patch(self, request, cliente_id):
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        entrada = ClienteEditarSerializer(cliente, data=request.data, partial=True)
        if not entrada.is_valid():
            return Response(
                {"estado": "error", "msg": "Error de validación", "errors": entrada.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            with transaction.atomic():
                entrada.save()
        except IntegrityError:
            return _error_response(
                "Ese teléfono ya está asociado a otro cliente.", status.HTTP_409_CONFLICT
            )
        cliente = obtener_clientes().get(pk=cliente_id)
        return Response({"estado": "ok", "data": ClienteSerializer(cliente).data})


class ClienteComprasView(APIView):
    def get(self, request, cliente_id):
        get_object_or_404(Cliente, pk=cliente_id)
        ventas = _ventas_queryset().filter(cliente_id=cliente_id).order_by("-fecha", "-id")
        return Response({"estado": "ok", "data": VentaSerializer(ventas, many=True).data})


class AbonosClienteView(APIView):
    def get(self, request, cliente_id):
        get_object_or_404(Cliente, pk=cliente_id)
        abonos = Abono.objects.filter(venta__cliente_id=cliente_id).select_related("venta")
        return Response({"estado": "ok", "data": AbonoSerializer(abonos, many=True).data})

    def post(self, request, cliente_id):
        entrada = CrearAbonoSerializer(data=request.data)
        if not entrada.is_valid():
            return Response(
                {"estado": "error", "msg": "Ingrese una venta y un abono entero positivo", "errors": entrada.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            abono = registrar_abono(
                cliente_id=cliente_id,
                venta_id=entrada.validated_data["venta_id"],
                monto=entrada.validated_data["monto"],
            )
        except VentaError as error:
            return _error_response(error)
        return Response(
            {"estado": "ok", "data": AbonoSerializer(abono).data},
            status=status.HTTP_201_CREATED,
        )
