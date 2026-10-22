from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.db import transaction
from .models import*

class PublicidadService:
    @staticmethod
    @transaction.atomic

    def obtener_publicidad():
        publicidadList = Publicidad.objects.filter().order_by('is_active')
        return publicidadList
    
    def obtener_publicidad_vigente():
        publicidadList = Publicidad.objects.filter('is_active').order_by('is_active')
        return publicidadList
    

class NewPublicidadService:
    @staticmethod
    @transaction.atomic
    def crear_publicidad(*,nombre, nombre_autor, telefono, descripcion, imagen):

        publicidad= Publicidad.objects.create(
            nombre=nombre,
            is_active=True,
            nombre_autor=nombre_autor,
            telefono=telefono,
            descripcion=descripcion,
            imagen=imagen
        )

        return 
    

class EditPublicidadService:
    @staticmethod
    @transaction.atomic
    def update_publicidad(*,id,nombre, nombre_autor, telefono, descripcion, imagen, is_active):

        publicidad = get_object_or_404(
            Publicidad,
            id=id
        )

        publicidad.nombre=nombre
        publicidad.is_active=is_active
        publicidad.nombre_autor=nombre_autor
        publicidad.telefono=telefono
        publicidad.descripcion=descripcion
        publicidad.imagen=imagen
        
        publicidad.save(update_fields=["nombre", "nombre_autor", "telefono", "descripcion", "imagen", "is_active"])

        return publicidad