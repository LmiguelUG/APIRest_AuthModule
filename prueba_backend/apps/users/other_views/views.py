from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from apps.users.models import User
from apps.users.other_views.serializers import LogoutSerializer, LoginSerializer


class Login(generics.GenericAPIView):
    
    def post(self, request):    
        try:
            user  = User.objects.filter(username = request.data['username']).get()
        except:
            return Response({'message':'Usuario no encontrado.'})
            
        if user:
            data = { 
                "username":user.username,
                "password":request.data["password"],
                "email":user.email
            }

            serializer = LoginSerializer(data = data)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'errors': serializer.errors}, status = status_HTTP_400_BAD_REQUEST)
            
                
class LogoutAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Logout exitoso."},status=status.HTTP_204_NO_CONTENT)