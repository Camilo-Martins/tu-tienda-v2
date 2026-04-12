from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import*
from personal.models import Persona
from .utils import horario_utils


#No borrar
class CreateHorarioService:
    @staticmethod
    @transaction.atomic
    def crear_horario():

        fecha_inicio, fecha_fin, nombre = horario_utils.calcular_semana_actual()
     
        horario_old = HorarioSemanal.objects.filter().order_by('-id').first()
        
        if horario_old:
            horario_old.is_active = False
            horario_old.save()

        horario = HorarioSemanal.objects.create(
                    nombre=nombre,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                )

        for dia in range(1,8):
            DiaHorario.objects.create(
                horario=horario,
                dia=dia
            )

        return horario

class GetHorarioService:
    @staticmethod
    @transaction.atomic
    def obtener_horario():

        horario = HorarioSemanal.objects.order_by('-id').first()
        dias = DiaHorario.objects.filter(horario=horario)

        return horario


class AsignarPersonalService:      
    @staticmethod
    @transaction.atomic  
    def asignar_semana( id, dia, personal):
      
        horario = get_object_or_404(
            HorarioSemanal,
            id=id
        )

        persona = get_object_or_404(
            Persona,
            id=personal,
         
        )

        dia = get_object_or_404(
            DiaHorario,
            horario=horario,
            id=int(dia)
        )

        asignacion = AsignacionDia.objects.create(
            dia=dia,
            persona=persona
         
        )

        return asignacion

class DesasginarPersonalService:      
    @staticmethod
    @transaction.atomic  
    def desasginar_semana( id, dia, personal):
      
        horario = get_object_or_404(
            HorarioSemanal,
            id=id
        )

        persona = get_object_or_404(
            Persona,
            id=personal,
        )

        dia = get_object_or_404(
            DiaHorario,
            horario=horario,
            id=int(dia)
        )

        asignacion = AsignacionDia.objects.filter(
            dia=dia,
            persona=persona
        ).delete()

        return asignacion


