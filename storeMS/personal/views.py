from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

#Locales
from .service import*
from .serializers import*

#Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.

class ObtenerEmpleados(APIView):
    @swagger_auto_schema(
            operation_description="Endpoint Obtener Empleados",
            responses={
                200:"Success",
                400:"Bad Request",
                500:"Internal Server Error"},)
    def get(self, request):

        try: 
            personalList = PersonalListService.obtener_empleados_por_admin()

            datos_json = EmpleadoSerializer(personalList, many=True)

            return Response({"estado":"ok", "data": datos_json.data}, status=status.HTTP_200_OK)

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

class ObtenerEmpleadosActivos(APIView):
    @swagger_auto_schema(
            operation_description="Endpoint Obtener Personal activo para la asignación de horario",
            responses={
                200:"Success",
                400:"Bad Request",
                500:"Internal Server Error"},)
    def get(self, request):

       
        try:
            personalList = PersonalActiveListService.obtener_empleados_por_admin()
            datos_json = PersonalActiveSerializer(personalList, many=True)
            return Response({"estado":"ok","data": datos_json.data},status=status.HTTP_200_OK)

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


class RegistroEmpleado(APIView):
    @swagger_auto_schema(
            operation_description="Endpoint Registro Empleado",
            responses={
                201:"Success",
                400:"Bad Request",
                500:"Internal Server Error"
            },
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'nombre_completo': openapi.Schema(type=openapi.TYPE_STRING, description="nombre_completo"),
                    'telefono': openapi.Schema(type=openapi.TYPE_STRING, description="telefono"),
                    'pago_diario': openapi.Schema(type=openapi.TYPE_INTEGER, description="pago_diario"),
                    'rut': openapi.Schema(type=openapi.TYPE_STRING, description="rut")
                },
                required=['nombre_completo', 'telefono']
            )
    )
    def post(self, request):
        serializer = NewPersonalSerializer(data=request.data)

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
            NewPersonalService.crear_empleado(
                **serializer.validated_data
            )

            return Response(
                {
                    "estado": "ok",
                    "msg": "Registro exitoso"
                },
                status=status.HTTP_201_CREATED
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

 
class EditarEmpleado(APIView):
    @swagger_auto_schema(
            operation_description="Endpoint Editar Personal",
            responses={
                200:"Success",
                400:"Bad Request",
                500:"Internal Server Error"
            },
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'nombre_completo': openapi.Schema(type=openapi.TYPE_STRING, description="nombre_completo"),
                    'telefono': openapi.Schema(type=openapi.TYPE_STRING, description="telefono"),

                    'pago_diario': openapi.Schema(type=openapi.TYPE_STRING, description="pago_diario"),
                    'rut': openapi.Schema(type=openapi.TYPE_STRING, description="rut")
                },
                required=['nombre_completo', 'telefono']
            )
    )
    def put(self, request, id):
        persona = Persona.objects.get(id=id)

        serializer = EditPersonalSerializer(
            persona,
            data=request.data
        )

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
            EditPersonalService.editar_empleado(
            
                id=id,
                **serializer.validated_data
            )

            return Response( {"estado": "ok", "data": "Estado actualizado"},status=200)
      
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
        