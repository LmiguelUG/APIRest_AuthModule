from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from apps.CRUDS.roles.models import Rol
from apps.CRUDS.roles.serializers import RolSerializer

@api_view(['GET', 'POST'])
def RolAPI(request):

    # List
    if request.method == 'GET':
        roles = Rol.objects.all()
        roles_serializer = RolSerializer(roles, many = True)
        return Response(roles_serializer.data, status = status.HTTP_200_OK)

    # Create
    if request.method == 'POST':
        rol_serializer = RolSerializer(data = request.data)
        if rol_serializer.is_valid():
            rol_serializer.save()
            return Response({"Message": "successfully created role", "Rol": rol_serializer.data}, status = status.HTTP_201_CREATED)
        
        return Response(rol_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET','PUT','DELETE'])
def RolDetailAPI(request,pk=None):
    rol = Rol.objects.filter(id=pk).first()

    if rol:
        # Retrieve
        if request.method == 'GET':
            roles_serializer = RolSerializer(rol)
            return Response(roles_serializer.data, status = status.HTTP_200_OK)
        
        # Update
        elif request.method == 'PUT':
            roles_serializer = RolSerializer(rol, data= request.data)
            if roles_serializer.is_valid():
                roles_serializer.save()
                return Response({"message": "successful role upgrade.","rol":roles_serializer.data}, status = status.HTTP_200_OK)
            return Response({"message": "error during role update.", "errors": roles_serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

        # Delete
        elif request.method == 'DELETE':
            print(rol)
            rol.delete()
            message = f'{rol} role removed successfully.'
        return Response({"message": message}, status = status.HTTP_200_OK)

    return Response({'message:': 'Role not found, check entered value'}, status = status.HTTP_400_BAD_REQUEST)