
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import os
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User

FACEBOOK_DEBUG_TOKEN_URL = "https://graph.facebook.com/debug_token"
FACEBOOK_ACCESS_TOKEN_URL = "https://graph.facebook.com/v7.0/oauth/access_token"
FACEBOOK_URL = "https://graph.facebook.com/"
CLIENT_ID="4276744392401466"
CLIENT_SECRET="bdeb4abaf871d6c147a2c7b7a6d987ae"

# https://www.facebook.com/v7.0/dialog/oauth?client_id=4276744392401466&redirect_uri=http://localhost:8000/accounts/facebook&state={%22{st=state123abc,ds=123456789}%22}&scope=email
class FacebookView(APIView):
    
    def get(self, request):
        # Token de acceso capturado desde el redireccionamiento de inicio de sesión de facebook
        # https://graph.facebook.com/v7.0/oauth/access_token?client_id={client_id}&redirect_uri=http://localhost:8000/accounts/facebook&client_secret={client_secret}&code={captured code}
        user_access_token_payload = {
            "client_id": CLIENT_ID,
            "redirect_uri": 'http://localhost:8000/accounts/facebook',
            "client_secret": CLIENT_SECRET,
            "code": request.GET.get("code"),
        }

        token_request = requests.get(FACEBOOK_ACCESS_TOKEN_URL, params=user_access_token_payload )
        access_token_response = json.loads(token_request.text)
        if "error" in access_token_response:
            return Response({'message': 'Token de acceso a facebook incorrecto/exipardo', 'error': access_token_response['error']}, status = status.HTTP_400_BAD_REQUEST)

        user_access_token = access_token_response["access_token"]

        # Token de accesso de facebook developers
        # https://graph.facebook.com/v7.0/oauth/access_token?client_id={cient_id}&client_secret={client_secret}&grant_type=client_credentials
        token_playload = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "client_credentials",
        }

        token_playload_request = requests.get(FACEBOOK_ACCESS_TOKEN_URL, params = token_playload)
        token_playload_response = json.loads(token_playload_request.text)
        if "error" in token_playload_response:
            return Response({"message": "Solicitud de token de acceso, no válida."}, status = status.HTTP_400_BAD_REQUEST)

        token_playload = token_playload_response["access_token"]
        # inspecionar validez del token de usuario
        # https://graph.facebook.com/debug_token?input_token={token-to-inspect}&access_token={app-token-or-admin-token}

        verify_access_token_playload = {
            "input_token" : user_access_token,
            "access_token": token_playload,
        }

        verify_token_request = requests.get(FACEBOOK_DEBUG_TOKEN_URL, params=verify_access_token_playload)
        verify_access_token_response = json.loads(verify_token_request.text)

        if "error" in verify_access_token_response:
            return Response({"message": "Token de acceso del usuario no verificado"}, status = status.HTTP_400_BAD_REQUEST)

        user_id = verify_access_token_response["data"]["user_id"]

        # obtención de 'email' de usuario
        # https://graph.facebook.com/{user_id}?fields=id,name,email&access_token={access_token}
        user_info_url = FACEBOOK_URL + user_id
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
            user.save()
            

        data = {
            "message": "Inicio de sesión con facebook exitosa.",
            "user": {"username": user.username, "email":user.email, "auth_provider":user.auth_provider},
            "tokens": user.tokens()
        }
        return Response(data, status = status.HTTP_200_OK)


class GoogleView(APIView):
    
    def post(self, request):
        payload = {'access_token': request.data.get("token")}
        request_ = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(request_.text)
        if 'error' in data:
            return Response({'message': 'Token de google incorrecto/expirado'}, status = status.HTTP_400_BAD_REQUEST)

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

        data = {
            "message": 'usuario logueado correctamente',
            "name": user.name,
            "last_name": user.last_name,
            "email": user.email,
            "password": user.password,
            "tokens": user.tokens()
        }

        return Response(data,status=status.HTTP_201_CREATED)