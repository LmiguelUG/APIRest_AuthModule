from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import generics, status, permissions, response
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import Util
import jwt

from authentication.models import User
# Serializers
from authentication.serializers import LoginSerializer, ProfileSerializer, RegisterSerializer, LogoutSerializer
from authentication.serializers import SetNewPasswordSerializer, ResetPasswordEmailRequestSerializer, UserTokenSerializer

class RegisterView(generics.GenericAPIView):
    
    authentication_classes = []
    serializer_class = RegisterSerializer

    def post(self, request):
        """ User registration in the system with username and password, and sending email to verify the email """
        
        serializer = self.serializer_class( data = request.data )
        if serializer.is_valid(): 
            serializer.save()
            user = User.objects.get( username = serializer.data['username'] )
            tokens = user.tokens()

            # -- CONSTRUCCIÓN DEL CORREO --
            current_site  = get_current_site(request).domain  # Obtengo el dominio de donde se hace la request
            relativeLink  = reverse('verify_email') # Enlace de redireccionamiento para verificación
            absolute_urls = 'http://'+ current_site + relativeLink +"?token="+str(tokens['access']) # URL absoluta para acceder desde el correo recibido
            email_body    = 'Hola, Bienvenido '+ user.username + '\nUsa este link para verificar tu registro. \n' + absolute_urls

            data = {'email_body': email_body, 'to_email': user.email,'email_subject': 'Verificación de cuenta'}
            Util.send_email(data)
            user_data = { "username": user.username, "email": user.email }
            
            return response.Response({"message": "check your mailbox, we have sent a verification email", "user": user_data}, status = status.HTTP_201_CREATED)
        
        return response.Response({"error": "unsuccessful user registration", "error": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

class VerifyEmailAPIView(generics.GenericAPIView):
    
    authentication_classes = []

    def get(self, request):
        """ check the token received in the url and set the email_verified field to True """
        token = request.GET.get('token')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        print(f'payload {payload}')
        user    = User.objects.get(id = payload['user_id'])
        
        if not user.email_verified:
            user.email_verified = True
            user.save()
            return response.Response({'email': "successful email verification"}, status = status.HTTP_200_OK)
        return response.Response({'error': "unsuccessful email verification"}, status = status.HTTP_400_BAD_REQUEST)
        
        

class LoginAPIView(generics.GenericAPIView):
    
    authentication_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        username    = request.data.get('username',)
        password = request.data.get('password',)
        user = authenticate(username = username, password = password)
        if user:
            serializer = self.serializer_class(user)
            return response.Response(serializer.data, status = status.HTTP_200_OK)

        return response.Response({"message": "invalid credentials, try again"}, status = status.HTTP_401_UNAUTHORIZED)


class ProfileAPIView(generics.GenericAPIView):
    
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """ the basic data (username, email) of the logged in user are obtained """
        user = request.user
        serializer = self.serializer_class(user)
        return response.Response({"user": serializer.data})


class LogoutAPIView (generics.GenericAPIView): 
    
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({'message:':'successful logout'},status=status.HTTP_204_NO_CONTENT)

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
                return response.Response({'error':'No match found in email search, verify.'})
        else:
            return response.Response({'error': reset_serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
        return response.Response({'message': 'check your email, you were sent a link to reset your password.'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id = id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return response.Response({'error':'Invalid token, request a new one'}, status=status.HTTP_400_BAD_REQUEST)
                
            return response.Response({'success':True,'message':'valid credentials', 'uidb64': uidb64,'token':token})
        
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return response.Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)
         
class SetNewPasswordAPIView(generics.GenericAPIView):

    def patch(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            return response.Response({'message':'successful password reset.'}, status=status.HTTP_200_OK)
        else:
            return response.Response({'errors': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)