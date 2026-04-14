from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.db import transaction
from .models import*


class ProductoService:
    @staticmethod
    @transaction.atomic

    def get_productos(*, proveedor=None, categoria=None):
        productos = Producto.objects.filter().order_by("-id")

        if proveedor:
            productos = productos.filter(proveedor__nombre_completo__icontains=proveedor)

        if categoria:
            productos = productos.filter(categoria=categoria)

        return productos
    
class NewProductoService:
    @staticmethod
    @transaction.atomic
    def crear_producto(*, nombre_producto, descripcion=None, precio=0, categoria=None, proveedor_id=None, stock_actual=0):

        print(proveedor_id)
        producto = Producto.objects.create(
            nombre_producto=nombre_producto,
            descripcion=descripcion,
            precio=precio,
            categoria=categoria,
            proveedor_id=proveedor_id,
            stock_actual=stock_actual,
            is_active=True,
        

        )

        return producto
    

class EditProductoService:
    @staticmethod
    @transaction.atomic
    def editar_producto(*,   id, nombre_producto=None, descripcion=None, precio=None, categoria=None, proveedor_id=None,
                        stock_actual=None, is_active=None):
        
        producto = get_object_or_404(
            Producto,
            id=id,
        )

        producto.nombre_producto = producto.nombre_producto = nombre_producto if nombre_producto else producto.nombre_producto
        producto.descripcion =  producto.descripcion = descripcion if descripcion else producto.descripcion
        producto.precio =  producto.precio = precio if precio else producto.precio
        producto.proveedor_id =  producto.proveedor_id = proveedor_id if proveedor_id else producto.proveedor_id
        producto.categoria =  producto.categoria = categoria if categoria else producto.categoria
        producto.stock_actual =  producto.stock_actual = stock_actual if stock_actual else producto.stock_actual
        producto.is_active =  producto.is_active = is_active if is_active else producto.is_active
        producto.save(update_fields=["nombre_producto", "descripcion", "precio", "categoria",  "stock_actual", "proveedor_id",
                                      "is_active"])
        return producto