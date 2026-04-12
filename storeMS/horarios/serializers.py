from rest_framework import serializers
from .models import*
from personal.serializers import*
from personal.models import Persona

class EmpleadoMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ["id", "nombre_completo", "telefono"]

class AsignacionSerializer(serializers.ModelSerializer):
    persona = EmpleadoMiniSerializer(read_only=True)
    class Meta:
        model = AsignacionDia
        fields = ["id", "persona", ]

class DiaHorarioSerializer(serializers.ModelSerializer):
    dia_nombre = serializers.CharField(source="get_dia_display")
    asignaciones = AsignacionSerializer(many=True, read_only=True)
    class Meta:
        model = DiaHorario
        fields = ["id", "dia", "dia_nombre", "asignaciones"]

class HorarioSerializer(serializers.ModelSerializer):
    dias = DiaHorarioSerializer(many=True, read_only=True)
    class Meta:
        model = HorarioSemanal
        fields = ("id", "nombre" , "is_active", "fecha_inicio", "fecha_fin", "dias")
 

class AsignarDiaSerializer(serializers.Serializer):
    id = serializers.IntegerField(  required=False,  )
    personal = serializers.IntegerField(  required=False, )
    dia = serializers.IntegerField( required=False,   )
    telefono = serializers.IntegerField( required=False,   )

    def validate_asignacion_dia(self,value):
        dia = self.context.get("dia")
        personal = self.context.get("personal")
        existe = AsignacionDia.objects.filter(
                dia=dia,
                personal=personal
            ).exists()

        if existe:
            raise serializers.ValidationError(
                "El personal ya está asignado a este día."
            )
        
        return existe

    def validate_asignacion(self,value):
        personal = self.context.get("personal")
        dia = self.context.get("dia")
        asignacion = AsignacionDia.objects.filter(personal=personal,dia=dia).exists()
        if asignacion:
            raise serializers.ValidationError("El Personal ya se encuentra asignado.")


        return asignacion