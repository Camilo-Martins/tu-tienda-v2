from rest_framework import serializers

from .models import Abono, Cliente, DetalleVenta, Venta
from .validators import normalize_phone


class ClienteEntradaSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=100, trim_whitespace=True)
    telefono = serializers.CharField(max_length=30, trim_whitespace=True)

    def validate_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError("Ingrese el nombre del cliente.")
        return value.strip()

    def validate_telefono(self, value):
        return normalize_phone(value)


class ClienteEditarSerializer(serializers.ModelSerializer):
    telefono = serializers.CharField(max_length=30, required=False)

    class Meta:
        model = Cliente
        fields = ["nombre", "telefono"]
        extra_kwargs = {"nombre": {"required": False}}

    def validate_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede quedar vacío.")
        return value.strip()

    def validate_telefono(self, value):
        telefono = normalize_phone(value)
        duplicate = Cliente.objects.filter(telefono=telefono)
        if self.instance:
            duplicate = duplicate.exclude(pk=self.instance.pk)
        if duplicate.exists():
            raise serializers.ValidationError(
                "Ese teléfono ya está asociado a otro cliente."
            )
        return telefono


class CrearAbonoSerializer(serializers.Serializer):
    venta_id = serializers.IntegerField(min_value=1)
    monto = serializers.IntegerField(min_value=1)


class ProductoVentaEntradaSerializer(serializers.Serializer):
    producto_id = serializers.IntegerField(min_value=1)
    cantidad = serializers.IntegerField(min_value=1)
    precio_esperado = serializers.IntegerField(min_value=0)


class CrearVentaSerializer(serializers.Serializer):
    tipo = serializers.ChoiceField(choices=Venta.Tipo.choices)
    items = ProductoVentaEntradaSerializer(many=True, allow_empty=False)
    cliente = ClienteEntradaSerializer(required=False, allow_null=True)

    def validate(self, attrs):
        if attrs["tipo"] == Venta.Tipo.FIADO and not attrs.get("cliente"):
            raise serializers.ValidationError(
                {"cliente": "Para fiar, ingrese nombre y teléfono del cliente."}
            )
        if attrs["tipo"] == Venta.Tipo.CONTADO and attrs.get("cliente"):
            raise serializers.ValidationError(
                {"cliente": "Una venta pagada no debe incluir datos de cliente."}
            )
        return attrs


class DetalleVentaSerializer(serializers.ModelSerializer):
    producto_id = serializers.IntegerField(read_only=True)
    nombre_producto = serializers.CharField(source="producto.nombre_producto", read_only=True)
    subtotal = serializers.IntegerField(read_only=True)

    class Meta:
        model = DetalleVenta
        fields = ["producto_id", "nombre_producto", "cantidad", "precio_unitario", "subtotal"]


class AbonoSerializer(serializers.ModelSerializer):
    venta_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Abono
        fields = ["id", "venta_id", "monto", "fecha"]
        read_only_fields = ["id", "fecha"]


class ClienteSerializer(serializers.ModelSerializer):
    saldo_pendiente = serializers.SerializerMethodField()
    estado = serializers.SerializerMethodField()

    class Meta:
        model = Cliente
        fields = ["id", "nombre", "telefono", "saldo_pendiente", "estado", "created_at"]

    def get_saldo_pendiente(self, obj):
        if hasattr(obj, "_saldo_pendiente"):
            return max(obj._saldo_pendiente, 0)
        return obj.saldo_pendiente

    def get_estado(self, obj):
        return "[con deuda*]" if self.get_saldo_pendiente(obj) > 0 else "[sin deudas]"


class ClienteResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ["id", "nombre", "telefono"]


class VentaSerializer(serializers.ModelSerializer):
    cliente = ClienteResumenSerializer(read_only=True)
    items = DetalleVentaSerializer(many=True, read_only=True)
    monto_abonado = serializers.SerializerMethodField()
    saldo_pendiente = serializers.SerializerMethodField()

    class Meta:
        model = Venta
        fields = [
            "id", "tipo", "fecha", "cliente", "items", "total",
            "monto_abonado", "saldo_pendiente",
        ]

    def get_monto_abonado(self, obj):
        if hasattr(obj, "_monto_abonado"):
            return obj._monto_abonado
        return sum(abono.monto for abono in obj.abonos.all())

    def get_saldo_pendiente(self, obj):
        if obj.tipo != Venta.Tipo.FIADO:
            return 0
        return max(obj.total - self.get_monto_abonado(obj), 0)
