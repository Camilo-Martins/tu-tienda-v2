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

class ObtenerProveedores(APIView):
    @swagger_auto_schema(
            operation_description="Endpoint Obtener todos los usuarios",
            responses={
                200:"Success",
                400:"Bad Request"},)
    def get(self, request):
        
        try:
        
            proveedoresLists = ProveedoresService.obtener_proveedores_por_admin()
            datos_json = ObtenerProveedoresSerializer(proveedoresLists, many=True)

            return Response({"estado":"ok","data": datos_json.data}, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response(
                {
                    "estado": "error",
                    "msg": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )



class ObtenerProveedoresListBox(APIView):
    @swagger_auto_schema(
            operation_description="Endpoint Obtener todos los usuarios activos",
            responses={
                200:"Success",
                400:"Bad Request"},)
    def get(self, request):
       
        try: 
     
            proveedoresLists = ProveedoresService.obtener_proveedores_por_admin_cbox()

            datos_json = ProveedoresListBoxSerializer(proveedoresLists, many=True)  

            return JsonResponse({"estado":"ok","data": datos_json.data},
                                 status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(
                {
                    "estado": "error",
                    "msg": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class AgregarProveedor(APIView):
    @swagger_auto_schema(
            operation_description="Endpoint Registro Proveedor",
            responses={
                201:"Success",
                400:"Bad Request",
                500:"Internal Server Error"
            },
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'nombre_completo': openapi.Schema(type=openapi.TYPE_STRING, description="nombre_completo"),
                    'nombre_empresa': openapi.Schema(type=openapi.TYPE_STRING, description="nombre_empresa"),
                    'telefono': openapi.Schema(type=openapi.TYPE_STRING, description="telefono"),
                    'rut': openapi.Schema(type=openapi.TYPE_STRING, description="rut"),
                    'observaciones': openapi.Schema(type=openapi.TYPE_STRING, description="observaciones"),
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description="email"),
                },
                required=['nombre_completo', 'telefono', 'email', 'nombre_empresa', 'rut']
            )
    )
    def post(self, request):

        serializer = NewProveedorSerializer( data=request.data)
        
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
            NewProveedorService.crear_proveedor(
                **serializer.validated_data
            )

            return JsonResponse({"estado": "ok", "msg": "Registro exitoso"},status=201)
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

class EditarProveedor(APIView):
    @swagger_auto_schema(
            operation_description="Endpoint Registro Proveedor",
            responses={
                201:"Success",
                400:"Bad Request",
                500:"Internal Server Error"
            },
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'nombre_completo': openapi.Schema(type=openapi.TYPE_STRING, description="nombre_completo"),
                    'nombre_empresa': openapi.Schema(type=openapi.TYPE_STRING, description="nombre_empresa"),
                    'telefono': openapi.Schema(type=openapi.TYPE_STRING, description="telefono"),
                    'rut': openapi.Schema(type=openapi.TYPE_STRING, description="rut"),
                    'observaciones': openapi.Schema(type=openapi.TYPE_STRING, description="observaciones"),
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description="email"),
                },
                required=['nombre_completo', 'telefono', 'email', 'nombre_empresa', 'rut']
            )
    )
    def put(self, request, id):
        proveedor = Proveedor.objects.get(id=id)
        serializer = EditProveedorSerializer(proveedor, data=request.data)
       
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
            EditProveedorService.editar_proveedor( 
                id=id,
                **serializer.validated_data
            )
            return Response({"estado": "ok", "msg": "Edición exitosa"},status=200)
        
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