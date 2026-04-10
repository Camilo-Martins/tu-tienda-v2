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

class ObtenerNotas(APIView):
    @swagger_auto_schema(
            operation_description="Endpoint Obtener notas",
            responses={
                200:"Success",
                400:"Bad Request"},)
    def get(self, request):

        try:
            notasLists = NotasService.obtener_notas_por_admin(
            )

            datos_json = ObtenerNotasSerializer(notasLists, many=True)

            return Response({"estado": "ok",
                             "data": datos_json.data},
                             status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(
                {
                    "estado": "error",
                    "msg": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class AgregarNota(APIView):
    @swagger_auto_schema(
            operation_description="Endpoint Agregar Nota",
            responses={
                201:"Created",
                400:"Bad Request",
                500:"Internal server error"
            },
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'nombre_nota': openapi.Schema(type=openapi.TYPE_STRING, description="nombre_nota"),
                    'observaciones': openapi.Schema(type=openapi.TYPE_STRING, description="observaciones")
                },
                required=['nombre_nota']
            )
    )
    def post(self, request):

        serializer = NewNotaSerializer(data=request.data)
        
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
            NewNotaService.crear_nota(
                **serializer.validated_data
            )

            return Response({"estado": "ok", "msg": "Registro exitoso"},status=201)
        
        except ValueError as e:
            return Response(
                {
                    "estado": "error",
                    "msg": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class EditarNota(APIView):
    @swagger_auto_schema(
            operation_description="Endpoint Editar Nota",
            responses={
                200:"Success",
                400:"Bad Request",
                500:"Internal server error"
            },
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'nombre_nota': openapi.Schema(type=openapi.TYPE_STRING, description="nombre_nota"),
            
                    'observaciones': openapi.Schema(type=openapi.TYPE_STRING, description="observaciones")
                },
                required=['nombre_nota']
            )
    )
    def put(self, request, id):

        serializer = EditNotaSerializer( data=request.data)
        
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
            EditNotaService.editar_nota( 
                id=id,
                **serializer.validated_data
            )

            return JsonResponse({"estado": "ok", "msg": "Nota Editada"},status=200)
        
        except ValueError as e:
            return Response(
                {
                    "estado": "error",
                    "msg": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )