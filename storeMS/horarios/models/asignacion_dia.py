from django.db import models
from .dia_horario import DiaHorario
from personal.models import Persona

class AsignacionDia(models.Model):
    dia = models.ForeignKey(
        DiaHorario,
        on_delete=models.CASCADE,
        related_name="asignaciones"
    )

    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("dia", "persona")