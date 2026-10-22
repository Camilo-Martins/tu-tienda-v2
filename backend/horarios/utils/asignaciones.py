from personal.models import Persona
from horarios.models import AsignacionDia, DiaHorario

def asignar_empleado_a_dia(dia, empleado_id):

    try:
        persona = Persona.objects.get(
            id=empleado_id,
            is_active=True
        )
    except Persona.DoesNotExist:
        return "Empleado no válido"

    # máximo 2 empleados por día
    if AsignacionDia.objects.filter(dia=dia).count() >= 2:
        return "Máximo de empleados alcanzado para este día"

    # no repetir empleado
    if AsignacionDia.objects.filter(dia=dia, persona=persona).exists():
        return "Empleado ya asignado a este día"

    AsignacionDia.objects.create(
        dia=dia,
        empleado=persona
    )

    return None
