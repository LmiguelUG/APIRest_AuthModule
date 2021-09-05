
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import os
from django.conf import settings
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User

# https://www.facebook.com/v7.0/dialog/oauth?client_id=4276744392401466&redirect_uri=http://localhost:8000/api/auth/social/facebook&state={%22{st=state123abc,ds=123456789}%22}&scope=email      
class FacebookAPIView(APIView):

    authentication_classes = []

    def get(self, request):
        # Token de acceso capturado desde el redireccionamiento de inicio de sesión de facebook
        # https://graph.facebook.com/v7.0/oauth/access_token?client_id={client_id}&redirect_uri=http://localhost:8000/api/auth/social/facebook&client_secret={client_secret}&code={captured code}
    
        user_access_token_payload = {
            "client_id": settings.CLIENT_ID,
            "redirect_uri": 'http://localhost:8000/api/auth/social/facebook',
            "client_secret": settings.CLIENT_SECRET,
            "code": request.GET.get("code"),
        }

        token_request = requests.get(settings.FACEBOOK_ACCESS_TOKEN_URL, params=user_access_token_payload )
        access_token_response = json.loads(token_request.text)
        if "error" in access_token_response:
            return Response({'error': access_token_response['error']}, status = status.HTTP_400_BAD_REQUEST)

        user_access_token = access_token_response["access_token"]

        # Token de accesso de facebook developers
        # https://graph.facebook.com/v7.0/oauth/access_token?client_id={cient_id}&client_secret={client_secret}&grant_type=client_credentials
        token_playload = {
            "client_id": settings.CLIENT_ID,
            "client_secret": settings.CLIENT_SECRET,
            "grant_type": "client_credentials",
        }

        token_playload_request = requests.get(settings.FACEBOOK_ACCESS_TOKEN_URL, params = token_playload)
        token_playload_response = json.loads(token_playload_request.text)
        if "error" in token_playload_response:
            return Response({"message": "Invalid access token request."}, status = status.HTTP_400_BAD_REQUEST)

        token_playload = token_playload_response["access_token"]
        # inspecionar validez del token de usuario
        # https://graph.facebook.com/debug_token?input_token={token-to-inspect}&access_token={app-token-or-admin-token}

        verify_access_token_playload = {
            "input_token" : user_access_token,
            "access_token": token_playload,
        }

        verify_token_request = requests.get(settings.FACEBOOK_DEBUG_TOKEN_URL, params=verify_access_token_playload)
        verify_access_token_response = json.loads(verify_token_request.text)

        if "error" in verify_access_token_response:
            return Response({"message": "Access token of the unverified user"}, status = status.HTTP_400_BAD_REQUEST)

        user_id = verify_access_token_response["data"]["user_id"]

        # obtención de 'email' de usuario
        # https://graph.facebook.com/{user_id}?fields=id,name,email&access_token={access_token}
        user_info_url = settings.FACEBOOK_URL + user_id
        user_info_payload = {
            "fields": "id,name,email",
            "access_token": user_access_token,
        }

        user_info_request  = requests.get(user_info_url, params=user_info_payload)
        user_info_response = json.loads(user_info_request.text)

        users_email = user_info_response["email"]

        # Crear usuario si no exite
        try:
            user = User.objects.get(email=user_info_response["email"])
        except User.DoesNotExist:
            user = User()
            user.username = user_info_response["email"]
            user.email = user_info_response["email"]
            # Contraseña predeterminada aleatoria
            user.password = make_password(BaseUserManager().make_random_password())
            user.auth_provider = 'facebook'
            user.is_activate = True
            user.save()
            

        data = {
            "message": "Login with facebook successful.",
            "user": {"username": user.username, "email":user.email, "auth_provider":user.auth_provider},
            "tokens": user.tokens()
        }
        return Response(data, status = status.HTTP_200_OK)


class GoogleAPIView(APIView):
    
    def post(self, request):
        payload = {'access_token': request.data.get("token")}
        # Google proporciona información del usuario a traves de la solicitud autorizada del siguiente enlace
        request_ = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(request_.text)
        if 'error' in data:
            return Response({'message': 'Bad / expired google token'}, status = status.HTTP_400_BAD_REQUEST)

        # Crear usuario si no existe
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            user = User()
            user.email = data['email']
            user.name  = data['given_name']
            user.last_name = data["family_name"]
            # Contraseña predeterminada aleatoria
            user.password = make_password(BaseUserManager().make_random_password())
            user.auth_provider = 'email'
            user.is_activate = True

        data = {
            "message": 'user successfully logged in',
            "name": user.name,
            "last_name": user.last_name,
            "email": user.email,
            "password": user.password,
            "tokens": user.tokens()
        }

        return Response(data,status=status.HTTP_201_CREATED)