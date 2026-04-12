from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import*

# services/empleado_service.py

   
class NewPersonalService:
    @staticmethod
    @transaction.atomic
    def crear_empleado(*, nombre_completo, telefono , rut=None, pago_diario=None):

        if not pago_diario or pago_diario == None:
            pago_diario = 0

        personal = Persona.objects.create(
            nombre_completo=nombre_completo,
            telefono=telefono,       
            pago_diario=pago_diario,
            rut=rut,
            is_active=True
           
        )

        return personal

class PersonalListService:
    staticmethod
    @transaction.atomic
    def obtener_empleados_por_admin():
        
        personalList = Persona.objects.order_by('-is_active')
        return personalList
  

class PersonalActiveListService:
    staticmethod
    @transaction.atomic
    def obtener_empleados_por_admin():
        
        personalList = Persona.objects.filter(is_active=True ).order_by('-is_active')
        return personalList
  


class EditPersonalService:
    @staticmethod
    @transaction.atomic
    def editar_empleado(*, id, nombre_completo, telefono, pago_diario=None, rut=None):
    
        empleado = get_object_or_404(
            Persona,
            id=id
        )
    
        if not pago_diario or pago_diario == None:
            pago_diario = 0

        empleado.nombre_completo=nombre_completo
        empleado.telefono=telefono
        empleado.pago_diario = pago_diario if pago_diario else empleado.pago_diario
        empleado.rut = rut if rut is not None else empleado.rut
        empleado.save(update_fields=["nombre_completo", "telefono", "pago_diario", "rut"])

        return empleado

