from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models.horario_semana import*
from .models.dia_horario import*

from .service import*
from .serializers import*

#Swagger
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

class ObtenerHorario(APIView):
    @swagger_auto_schema(
            operation_description="Endpoint Obtener horario por ID",
            responses={
                200:"Success",
                400:"Bad Request",
                500:"Internal Server Error"
            },
    )
    def get(self, request):
    
        try: 
            horario= GetHorarioService.obtener_horario()

            datos_json= HorarioSerializer(horario)

            return Response({"estado":"ok", "data":datos_json.data} ,status=status.HTTP_200_OK)
       
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
        
class CrearHorario(APIView):
    @swagger_auto_schema(
            operation_description="Endpoint Creacion Horario ( Forma manual )",
            responses={
                201:"Success",
                400:"Bad Request",
                500:"Internal Server Error"
            },
    )
    def post(self, request):
        
        try: 
            CreateHorarioService.crear_horario()
            
            return Response(
                    {"estado": "ok", "msg": "Horario Creado"},
                    status=status.HTTP_200_OK
                )

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
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AsignarSemana(APIView):
    @swagger_auto_schema(
            operation_description="Endpoint Creacion Horario ( Forma manual )",
            responses={
                201:"Success",
                400:"Bad Request",
                500:"Internal Server Error"
            },
    )
    def post(self, request, id):
      
        serializer = AsignarDiaSerializer(data={ "id":id,  "data":request.data})
        serializer.is_valid(raise_exception=True)

        try: 
            AsignarPersonalService.asignar_semana(
                    id=id,
                    dia=request.data.get("dia"),
                    personal=request.data.get("personal"),
            )
            
            return Response(
                    {"estado": "ok", "msg": "Horario Creado"},
                status=status.HTTP_200_OK
                )

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
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DesasignarSemana(APIView):
    @swagger_auto_schema(
            operation_description="Endpoint Creacion Horario ( Forma manual )",
            responses={
                201:"Success",
                400:"Bad Request",
                500:"Internal Server Error"
            },
    )
   
    def post(self, request, id):
    
         
        serializer = AsignarDiaSerializer(data={ "id":id,  "data":request.data})
        serializer.is_valid(raise_exception=True)

        try: 
            DesasginarPersonalService.desasginar_semana(
                
                    id=id,
                    dia=request.data.get("dia"),
                    personal=request.data.get("personal"),
            )

            return  Response(
                {"estado": "ok", "msg": "Horario Creado"},
                status=201
            )

        except ValueError as e:
            return Response(
                {
                    "estado": "error",
                    "msg": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception:
            return Response(
                {
                    "estado": "error",
                    "msg": "Ocurrió un error interno"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

      