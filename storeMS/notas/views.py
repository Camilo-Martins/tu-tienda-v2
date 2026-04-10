from rest_framework.views import APIView
from django.http.response import JsonResponse

#Locales

from .services import*
from .serializers import*

# Create your views here.

class ObtenerNotas(APIView):
    def get(self):

        serializer = ObtenerNotasSerializer()
        serializer.is_valid(raise_exception=True)

        notasLists = NotasService.obtener_notas_por_admin(
            **serializer.validated_data
        )

        datos_json = ObtenerNotasSerializer(notasLists, many=True)

        return JsonResponse({"data": datos_json.data})
    
class AgregarNota(APIView):
    def post(self, request):

        serializer = NewNotaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        NewNotaService.crear_nota(
            **serializer.validated_data
        )

        return JsonResponse({"estado": "ok", "msg": "Registro exitoso"},status=201)
    
class EditarNota(APIView):
  
    def put(self, request, id):

        serializer = EditNotaSerializer( data=request.data)
        serializer.is_valid(raise_exception=True)

        EditNotaService.editar_nota( 
            id=id,
            **serializer.validated_data
        )

        return JsonResponse({"estado": "ok", "msg": "Nota Editada"},status=200)