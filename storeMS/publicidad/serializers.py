from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import Publicidad

class PublicidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicidad
        fields = "__all__"

class NewPublicidadSerializer(serializers.Serializer):

    nombre = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=30,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ,.:]+$',
                message="El nombre solo puede contener letras, números y espacios."
            )
        ]
    )
    
    descripcion = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ,.:]+$',
                message="La descripción solo puede contener letras, números y espacios."
            )
        ]
    )

    nombre_autor = serializers.CharField(
        required=False,
        allow_blank=True,
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

    imagen = serializers.ImageField(required=True)


class EditPublicidadSerializer(serializers.Serializer):

    nombre = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=30,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ,.:]+$',
                message="El nombre solo puede contener letras, números y espacios."
            )
        ]
    )
    
    descripcion = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ,.:]+$',
                message="La descripción solo puede contener letras, números y espacios."
            )
        ]
    )

    nombre_autor = serializers.CharField(
        required=False,
        allow_blank=True,
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

    imagen = serializers.ImageField(required=True)
    is_active = serializers.BooleanField(required=False, allow_null=False)