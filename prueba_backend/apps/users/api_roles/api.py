from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from apps.users.models import Rol
from apps.users.api_roles.serializers import RolSerializer

@api_view(['GET', 'POST'])
def roles_api_view(request):

    # Listar
    if request.method == 'GET':
        roles = Rol.objects.all()
        roles_serializer = RolSerializer(roles, many = True)
        return Response(roles_serializer.data, status = status.HTTP_200_OK)

    # Creación
    if request.method == 'POST':
        rol_serializer = RolSerializer(data = request.data)
        if rol_serializer.is_valid():
            rol_serializer.save()
            return Response({"Message": "Rol creado correctamente", "Rol": rol_serializer.data}, status = status.HTTP_201_CREATED)
        
        return Response(rol_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET','PUT','DELETE'])
def rol_detail_api_view(request,pk=None):
    rol = Rol.objects.filter(id=pk).first()

    if rol:
        # Obtener
        if request.method == 'GET':
            roles_serializer = RolSerializer(rol)
            return Response(roles_serializer.data, status = status.HTTP_200_OK)
        
        # Actualizar
        elif request.method == 'PUT':
            roles_serializer = RolSerializer(rol, data= request.data)
            if roles_serializer.is_valid():
                roles_serializer.save()
                return Response({"message": "Actualización de rol exitosa.","rol":roles_serializer.data}, status = status.HTTP_200_OK)
            return Response({"message": "error durante la actualización del rol.", "errors": roles_serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

        # Eliminar
        elif request.method == 'DELETE':
            print(rol)
            rol.delete()
            message = f'Rol {rol} eliminado exitosamente.'
        return Response({"message": message}, status = status.HTTP_200_OK)

    return Response({'message:': 'Rol no encontrado, verifica valor ingresado'}, status = status.HTTP_400_BAD_REQUEST)