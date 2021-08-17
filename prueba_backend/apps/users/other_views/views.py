from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from apps.users.models import User
from apps.users.users.serializers import UserSerializer
from apps.users.other_views.serializers import LogoutSerializer, LoginSerializer, RegisterSerializer

class RegisterView(generics.GenericAPIView):

    def post(self, request):    
        users_serializer = RegisterSerializer(data = request.data)
        if users_serializer.is_valid(): 
            users_serializer.save()
            user_data = users_serializer.data
            user = User.objects.get(email=user_data['email'])

            data = { "username": user.username, "email": user.email, 'name':user.name, "last_name":user.last_name, 'tokens': user.tokens()}
            return Response({"message": "usuario registrado correctamente", "user": data}, status = status.HTTP_201_CREATED)
        return Response({"message": "error durante el registro de usuario", "error": users_serializer.errors}, status = status.HTTP_400_BAD_REQUEST)


class Login(generics.GenericAPIView):
    
    def post(self, request):
        # verificación de usuario registrado
        try:
            user  = User.objects.filter(username = request.data['username']).get()
        except:
            return Response({'message':'Usuario no encontrado.'})
         
        if user:
            data  = { 
                    "username":user.username,
                    "password":request.data["password"],
                    "email": user.email
            }

            serializer = LoginSerializer(data = data)
            if serializer.is_valid():
                user_username = User.objects.filter(username = data['username'])
                user_auth     = authenticate(email=data['email'], password=data['password'])
        
                if user_username.exists() and user_username[0].auth_provider != 'username':
                    conflict = {'conflict': 'Continúe con su inicio de sesión usando ' + user_username[0].auth_provider}
                    return Response({'conflict': conflict}, status = status.HTTP_409_CONFLICT)

                if not user_auth:
                    return Response('Contraseña Incorrecta.', status = status.HTTP_400_BAD_REQUEST)
                 
                if not user_auth.is_active:
                    return Response({'error': 'Usuario bloqueado, contacte al admin.'}, status = status.HTTP_400_BAD_REQUEST)

                data_ =  {
                    'email': user_auth.email,
                    'username': user_auth.username,
                    'tokens': user_auth.tokens(),
                    'auth_provider': user_auth.auth_provider
                }
                return Response({"message": "inicio de seción exitoso", "user": data_}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Datos incorrectos, veriquelos.'}, status = status.HTTP_400_BAD_REQUEST)
            
                
class LogoutAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message":"cierre de sesión exitoso."},status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST )
        