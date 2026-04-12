from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework import status

#Locales
from .services import*
from .serializers import*

#Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



# Create your views here.
class ObtenerProductos(APIView):
    @swagger_auto_schema(
            operation_description="Endpoint Obtener todos productos",
            responses={
                200:"Success",
                400:"Bad Request"},)
    def get(self, request):
      
        try:
            proveedor = request.query_params.get('proveedor')
            categoria = request.query_params.get('categoria')

            productosList = ProductoService.get_productos(
            
                proveedor=proveedor,
                categoria=categoria
            )

            datos_json = ProductoSerializer(productosList, many=True)

            return Response({"estado":"ok", "msg": datos_json.data}, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return Response(
                {
                    "estado": "error",
                    "msg": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class AgregarProducto(APIView):
  
    @swagger_auto_schema(
            operation_description="Endpoint Registro Producto",
            responses={
                201:"Success",
                400:"Bad Request",
                500:"Internal Server Error"
            },
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'nombre_producto': openapi.Schema(type=openapi.TYPE_STRING, description="nombre_producto"),
                    'proveedor': openapi.Schema(type=openapi.TYPE_STRING, description="proveedor"),
                    'descripcion': openapi.Schema(type=openapi.TYPE_STRING, description="descripcion"),
                    'precio': openapi.Schema(type=openapi.TYPE_STRING, description="precio"),
                    'stock_actual': openapi.Schema(type=openapi.TYPE_STRING, description="stock_actual"),
                    'categoria': openapi.Schema(type=openapi.TYPE_STRING, description="categoria"),
                },
                required=['nombre_producto']
            )
    )
    def post(self, request):
        serializer = NewProductoSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "estado": "error",
                    "msg": "Error de validación",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            NewProductoService.crear_producto(
                **serializer.validated_data
            
            )
            return JsonResponse({"estado":"ok","msg": "Producto agregado"}, status=201)
        
        except ValueError as e:
            return Response(
                {
                    "estado": "error",
                    "msg": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except ValueError as e:
            return Response(
                {
                    "estado": "error",
                    "msg": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class EditarProducto(APIView):
    @swagger_auto_schema(
            operation_description="Endpoint Editar Producto",
            responses={
                201:"Success",
                400:"Bad Request",
                500:"Internal Server Error"
            },
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'nombre_producto': openapi.Schema(type=openapi.TYPE_STRING, description="nombre_producto"),
                    'proveedor': openapi.Schema(type=openapi.TYPE_STRING, description="proveedor"),
                    'descripcion': openapi.Schema(type=openapi.TYPE_STRING, description="descripcion"),
                    'precio': openapi.Schema(type=openapi.TYPE_STRING, description="precio"),
                    'stock_actual': openapi.Schema(type=openapi.TYPE_STRING, description="stock_actual"),
                    'categoria': openapi.Schema(type=openapi.TYPE_STRING, description="categoria"),
                },
                required=['nombre_producto', 'proveedor']
            )
    )
    def put(self, request, id):

        serializer = EditarProductoSerializer( data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "estado": "error",
                    "msg": "Error de validación",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try: 
            EditProductoService.editar_producto(
            **serializer.validated_data,
            id=id)

            return JsonResponse({"estado":"ok", "msg": "Producto editado correctamente"}, status=200)

        except ValueError as e:
            return Response(
                {
                    "estado": "error",
                    "msg": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except ValueError as e:
            return Response(
                {
                    "estado": "error",
                    "msg": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )