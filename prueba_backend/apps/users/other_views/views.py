from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from apps.users.models import User
from apps.users.users.serializers import UserSerializer
from apps.users.other_views.serializers import LogoutSerializer, LoginSerializer, RegisterSerializer, SetNewPasswordSerializer, ResetPasswordEmailRequestSerializer
from .utils import Util
from django.urls import reverse
import jwt
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site 
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode




class VerifyEmailAPIView(generics.GenericAPIView):
    
    def get(self, request):
        token = request.GET.get('token')
        try:
            print(settings.SECRET_KEY)
            payload=jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user=User.objects.get(id=payload['user_id'])
            if not user.is_activate:
                user.is_activate = True
                user.save()
            return Response({'email': "Activacion de cuenta satisfactoria"}, status = status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activación expirada'}, status = status.HTTP_400_BAD_REQUEST)     
        except jwt.exceptions.DecodeError as identifier:
            print(identifier)
            return Response({'error': 'Token invalido'}, status = status.HTTP_400_BAD_REQUEST)     
        
class RegisterView(generics.GenericAPIView):

    def post(self, request):    
        users_serializer = RegisterSerializer(data = request.data)
        if users_serializer.is_valid(): 
            users_serializer.save()
            user_data = users_serializer.data
            user = User.objects.get(email=user_data['email'])
            
            # Envio de correo de virificación
            tokens = user.tokens()
            # Obtengo el dominio de donde se hace la request
            current_site = get_current_site(request).domain
            relativeLink = reverse('verify_email')
            absolute_urls = 'http://'+current_site+relativeLink+"?token="+str(tokens['access'])
            email_body = 'Hola, Bienvenido '+user.username + \
                         'Usa este link para verificar tu registro. \n' + absolute_urls

            data = {'email_body': email_body, 'to_email': user.email,'email_subject': 'verifica tu cuenta'}
            Util.send_email(data)

            data_ = { "username": user.username, "email": user.email, 'name':user.name, "last_name":user.last_name, 'tokens': tokens}
            return Response({"message": "usuario registrado correctamente", "user": data_}, status = status.HTTP_201_CREATED)
        return Response({"message": "error durante el registro de usuario", "error": users_serializer.errors}, status = status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    
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


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    def post(self, request):
        reset_serializer = self.serializer_class(data=request.data)

        if reset_serializer.is_valid():
            
            email = request.data.get('email', '')
            if User.objects.filter(email=email).exists():
                user   = User.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                token  = PasswordResetTokenGenerator().make_token(user)
                # -- Creación de url de petición --
                # Obtengo dominio de la request
                current_site = get_current_site(request=request).domain
                relativeLink = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
                absolute_url = 'http://'+current_site + relativeLink

                email_body   = 'Hola ' + user.username + ' usa este link para reestablecimiento de su contraseña \n' + \
                                absolute_url

                # datos necesarios para envio de correo
                data = {'email_body': email_body, 'to_email': user.email,'email_subject': 'Reseteo de contraseña.'}
                Util.send_email(data)
            else:
                return Response({'error':'No se encontró coincidencia en la busqueda del correo, verificar. '})
        else:
            return Response({'error': reset_serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
        return Response({'success': 'revise su correo, se le envió un enlace para restablecer su contraseña.'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error':'token no valido, solicite uno nuevo'}, status=status.HTTP_400_BAD_REQUEST)
                
            return Response({'success':True,'message':'credenciales validas', 'uidb64': uidb64,'token':token})
        
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)
         
class SetNewPasswordAPIView(generics.GenericAPIView):

    def patch(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'success': True,'message':'reestablecimiento de contraseña exitoso.'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)