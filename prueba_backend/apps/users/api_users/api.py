from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from apps.users.api_users.serializers import UserSerializer, UserListSerializer
from apps.users.models import User

@api_view(['GET','POST'])
def user_api_view(request):

    # Listar
    if request.method == 'GET':
        users = User.objects.all().values('id','username','email','name','last_name')
        users_serializer = UserListSerializer(users, many = True)
        return Response({"users": users_serializer.data}, status = status.HTTP_200_OK)

    # Creación
    elif request.method == 'POST':
        
         # Si aprueba las validaciones para el modelo de usuario, guardo en la BD o retorno algún error, de existir
        users_serializer = UserSerializer(data = request.data)
        if users_serializer.is_valid(): 
            users_serializer.save()
            return Response({"message": "usuario registrado correctamente", "user": users_serializer.data}, status = status.HTTP_201_CREATED)

        return Response({"message": "error durante la creación de usuario", "error": users_serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def user_detail_api_view(request,pk=None):
    user = User.objects.filter(id=pk).first()

    if user:
        # Optener
        if request.method == 'GET':
            users_serializer = UserSerializer(user)
            return Response({"user": users_serializer.data}, status = status.HTTP_200_OK)
        
        # Actualizar
        elif request.method == 'PUT':
            users_serializer = UserSerializer(user, data= request.data)
            if users_serializer.is_valid():
                users_serializer.save()
                return Response(users_serializer.data, status = status.HTTP_200_OK)
            return Response(users_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        # Eliminiar
        elif request.method == 'DELETE':
            user.delete()
            message = f'eliminado {user.username} correctamente'
            return Response({"message": message}, status = status.HTTP_200_OK)

    return Response({'message:': 'Usuario no encontrado, petición incorrecta'}, status = status.HTTP_400_BAD_REQUEST)