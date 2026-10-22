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
from django.shortcuts import render

# Create your views here.

class ObtenerPublicidad(APIView):
    def get(self, request):
        try:
            publicidadList = PublicidadService.obtener_publicidad()
            datos_json = PublicidadSerializer(publicidadList, many=True)

            return JsonResponse({"estado": "ok",
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
        
class ObtenerPublicidadVigente(APIView):
    def get(self, request):
        try:
            publicidadList = PublicidadService.obtener_publicidad()
            datos_json = PublicidadSerializer(publicidadList, many=True)

            return JsonResponse({"estado": "ok",
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
        
class AgregarPublicidad(APIView):
     
    def post(self, request):
        serializer = NewPublicidadSerializer(data=request.data)
            
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
            NewPublicidadService.crear_publicidad(
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
        
class EditarPublicidad(APIView):
    def put(self, request, id):
     
        serializer = EditPublicidadSerializer(data=request.data)

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
            EditPublicidadService.update_publicidad(
                id=id,
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