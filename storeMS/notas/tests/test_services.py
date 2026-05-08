import pytest

from django.core.exceptions import ValidationError

from notas.models import Nota
from notas.services import (
    NewNotaService,
    EditNotaService,
)


@pytest.mark.django_db
class TestNewNotaService:

    def test_create_note_successfully(self):

        nota = NewNotaService.crear_nota(
            nombre_nota="Nota importante",
            observaciones="Observacion de prueba"
        )

        assert nota.id is not None
        assert nota.nombre_nota == "Nota importante"
        assert nota.observaciones == "Observacion de prueba"
        assert nota.is_active is True

    def test_create_note_requires_name(self):

        with pytest.raises(ValidationError):

            NewNotaService.crear_nota(
                nombre_nota=None
            )


@pytest.mark.django_db
class TestEditNotaService:

    def test_edit_note_name(self):

        nota = Nota.objects.create(
            nombre_nota="Nombre viejo",
            observaciones="Texto viejo",
            is_active=True
        )

        updated_nota = EditNotaService.editar_nota(
            id=nota.id,
            nombre_nota="Nombre nuevo"
        )

        assert updated_nota.nombre_nota == "Nombre nuevo"

    def test_edit_note_keeps_original_values(self):

        nota = Nota.objects.create(
            nombre_nota="Original",
            observaciones="Observacion original",
            is_active=True
        )

        updated_nota = EditNotaService.editar_nota(
            id=nota.id,
            nombre_nota="Actualizado"
        )

        assert updated_nota.nombre_nota == "Actualizado"
        assert updated_nota.observaciones == "Observacion original"
        assert updated_nota.is_active is True