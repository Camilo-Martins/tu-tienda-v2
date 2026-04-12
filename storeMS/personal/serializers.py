from rest_framework import serializers
from .models import Persona
import re
from django.core.validators import RegexValidator

#Obtiene todos los empleado
class EmpleadoSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d/%m/%Y")#13/10/2025
     
    class Meta:
        model = Persona
        fields = ("id", "nombre_completo", "telefono", "rut",
                 "is_active", "pago_diario", "created_at")
        

#Crea un nuevo personal
#Validaciones estrictas para los campos rut y telefono
class NewPersonalSerializer(serializers.Serializer):
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
                message="El teléfono debe contener exactamente 8 dígitos."
            )
        ]
    )

    pago_diario = serializers.CharField(
        required=False,
        allow_blank=True
    )

    rut = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=12
    )

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

        if Persona.objects.filter(telefono=telefono_limpio).exists():
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

        if Persona.objects.filter(rut=rut_formateado).exists():
            raise serializers.ValidationError("Ya existe una persona con este RUT.")

        return rut_formateado
    

#Obtiene todas las persenos activas
#Necesario para el select del horario
class PersonalActiveSerializer(serializers.Serializer):
  
    id = serializers.CharField(required=False, allow_blank=True)
    nombre_completo = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = Persona
        fields = ["id", "nombre_completo"]


class EditPersonalSerializer(serializers.Serializer):
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
                message="El teléfono debe contener exactamente 8 dígitos."
            )
        ]
    )

    pago_diario = serializers.CharField(
        required=False,
        allow_blank=True
    )

    rut = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=12
    )

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

        if Persona.objects.filter(telefono=telefono_limpio).exists():
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

        if Persona.objects.filter(rut=rut_formateado).exists():
            raise serializers.ValidationError("Ya existe una persona con este RUT.")

        return rut_formateado
    