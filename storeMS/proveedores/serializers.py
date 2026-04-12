from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import Proveedor
import re

class ProveedorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proveedor
        fields = ("id", "nombre_completo", "telefono", "email", "rut", 
                  "nombre_empresa", "is_active", "observaciones", "created_at")

class ObtenerProveedoresSerializer(serializers.Serializer):


    id = serializers.CharField(required=False, allow_blank=True)
    nombre_completo = serializers.CharField(required=False, allow_blank=True)
    telefono = serializers.CharField(required=False, allow_blank=True)          
    email = serializers.EmailField(required=False, allow_blank=True)
    rut = serializers.CharField(required=False, allow_blank=True)
    nombre_empresa = serializers.CharField(required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False)
    observaciones = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Proveedor
        fields = ("id", "nombre_completo", "telefono", "email", "rut", 
                  "nombre_empresa",  "is_active", "observaciones", "created_at")

class NewProveedorSerializer(serializers.Serializer):
    
    nombre_completo = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$',
                message="El nombre solo puede contener letras, números y espacios."
            )
        ]
    )

    telefono = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=8,
        min_length=8,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{8,12}$',
                message="El teléfono debe contener entre 8 y 12 dígitos."
            )
        ]
    )

    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[\w\.-]+@[\w\.-]+\.\w+$',
                message="Ingrese un correo electrónico válido."
            )
        ])
    
    rut = serializers.CharField(
        required=False,     
        allow_blank=True,
        max_length=13,
       )
    
    nombre_empresa = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$',
                message="El nombre solo puede contener letras, números y espacios."
            )
        ]
    )

    observaciones = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$',
                message="La obsercación solo puede contener letras, números y espacios."
            )
        ]
    )

    is_active = serializers.BooleanField(required=False, allow_null=False)

 

    def validate_telefono(self, value):
        """
        Reglas:
        - Campo opcional
        - Si viene informado, debe tener exactamente 8 dígitos
        - Se guarda sin +569
        """
        if value is None or value.strip() == "":
            return ""

        telefono_limpio = value.strip()

        if Proveedor.objects.filter(telefono=telefono_limpio).exists():
            raise serializers.ValidationError("Ya existe una persona con este teléfono.")

        return telefono_limpio

    def _clean_rut(self, rut: str) -> str:
        """
        Elimina puntos, guión, espacios y deja DV en mayúscula.
        Ejemplo:
        '12.345.678-k' -> '12345678K'
        """
        rut = rut.strip().upper()
        rut = re.sub(r'[^0-9K]', '', rut)
        return rut

    def _is_valid_rut_structure(self, rut: str) -> bool:
        """
        Debe tener al menos cuerpo + DV.
        Ejemplo válido estructuralmente:
        12345678K
        1234567K
        """
        return bool(re.fullmatch(r'^\d{7,8}[0-9K]$', rut))

    def _is_valid_rut_dv(self, rut: str) -> bool:
        """
        Valida dígito verificador chileno.
        """

        dv_ingresado = rut[-1]
        dv = dv_ingresado.strip().upper()

        if dv == 'K' or dv.isdigit():
            return dv

    def _format_rut(self, rut: str) -> str:
        """
        Convierte:
        12345678K -> 12.345.678-K
        1234567K  -> 1.234.567-K
        """
        cuerpo = rut[:-1]
        dv = rut[-1]

        cuerpo_formateado = f"{int(cuerpo):,}".replace(",", ".")

        return f"{cuerpo_formateado}-{dv}"
   
    def validate_rut(self, value):
        """
        Reglas:
        - Campo opcional
        - Si viene informado, se valida y se normaliza
        - Se guarda en formato chileno estándar: XX.XXX.XXX-X
        """
        if value is None or value.strip() == "":
            return ""

        rut_limpio = self._clean_rut(value)

        if not self._is_valid_rut_structure(rut_limpio):
            raise serializers.ValidationError("El formato del RUT no es válido.")

        if not self._is_valid_rut_dv(rut_limpio):
            raise serializers.ValidationError("El DV ingresado no es válido.")

        rut_formateado = self._format_rut(rut_limpio)

        if Proveedor.objects.filter(rut=rut_formateado).exists():
            raise serializers.ValidationError("Ya existe una persona con este RUT.")

        return rut_formateado
    
    def validate_email(self, value):
        if Proveedor.objects.filter(email=value).exists():
            raise serializers.ValidationError("El correo electrónico ingresado ya existe.")
        return value


class EditProveedorSerializer(serializers.Serializer):
    nombre_completo = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$',
                message="El nombre solo puede contener letras, números y espacios."
            )
        ]
    )

    telefono = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{8,12}$',
                message="El teléfono debe contener entre 8 y 12 dígitos."
            )
        ]
    )

    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[\w\.-]+@[\w\.-]+\.\w+$',
                message="Ingrese un correo electrónico válido."
            )
        ])
    
    rut = serializers.CharField(
        required=False,     
        allow_blank=True,
        max_length=12,
       )
    
    nombre_empresa = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$',
                message="El nombre solo puede contener letras, números y espacios."
            )
        ]
    )

    observaciones = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$',
                message="La obsercación solo puede contener letras, números y espacios."
            )
        ]
    )

    is_active = serializers.BooleanField(required=False, allow_null=False)

    def validate_rut(self, value):
        """
        Reglas:
        - Campo opcional
        - Si viene informado, se valida y se normaliza
        - Se guarda en formato chileno estándar: XX.XXX.XXX-X
        """
        if value is None or value.strip() == "":
            return ""

        rut_limpio = self._clean_rut(value)

        if not self._is_valid_rut_structure(rut_limpio):
            raise serializers.ValidationError("El formato del RUT no es válido.")

        if not self._is_valid_rut_dv(rut_limpio):
            raise serializers.ValidationError("El RUT ingresado no es válido.")

        rut_formateado = self._format_rut(rut_limpio)

        queryset = Proveedor.objects.filter(rut=rut_formateado)

        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.exists():
            raise serializers.ValidationError("Ya existe un proveedor con este RUT.")

        return rut_formateado

    def validate_telefono(self, value):
        """
        Reglas:
        - Campo opcional
        - Si viene informado, debe tener exactamente 8 dígitos
        - Se guarda sin +569
        """
        if value is None or value.strip() == "":
            return ""

        telefono_limpio = value.strip()

        queryset = Proveedor.objects.filter(telefono=value)

        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.exists():
            raise serializers.ValidationError("El telefono ya existe.")

        return telefono_limpio

    def _clean_rut(self, rut: str) -> str:
        """
        Elimina puntos, guión, espacios y deja DV en mayúscula.
        Ejemplo:
        '12.345.678-k' -> '12345678K'
        """
        rut = rut.strip().upper()
        rut = re.sub(r'[^0-9K]', '', rut)
        return rut

    def _is_valid_rut_structure(self, rut: str) -> bool:
        """
        Debe tener al menos cuerpo + DV.
        Ejemplo válido estructuralmente:
        12345678K
        1234567K
        """
        return bool(re.fullmatch(r'^\d{7,8}[0-9K]$', rut))

    def _is_valid_rut_dv(self, rut: str) -> bool:
        """
        Valida dígito verificador chileno.
        """

        dv_ingresado = rut[-1]
        dv = dv_ingresado.strip().upper()

        if dv == 'K' or dv.isdigit():
            return dv


    def _format_rut(self, rut: str) -> str:
        """
        Convierte:
        12345678K -> 12.345.678-K
        1234567K  -> 1.234.567-K
        """
        cuerpo = rut[:-1]
        dv = rut[-1]

        cuerpo_formateado = f"{int(cuerpo):,}".replace(",", ".")

        return f"{cuerpo_formateado}-{dv}"
   
    def validate_email(self, value):
        
        queryset = Proveedor.objects.filter(email=value)

        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.exists():
            raise serializers.ValidationError("El correo electrónico ingresado ya existe.")

        return value
    
class ProveedoresListBoxSerializer(serializers.Serializer):

    id = serializers.CharField(required=False, allow_blank=True)
    nombre_empresa = serializers.CharField(required=False, allow_blank=True)
    nombre_completo = serializers.CharField(required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False)
    telefono = serializers.CharField(required=False, allow_blank=True)          
    email = serializers.EmailField(required=False, allow_blank=True)

    class Meta:
        model = Proveedor
        fields = ("id", "nombre_completo", "nombre_empresa", "is_active", "telefono", "email")