from django.shortcuts import render
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from apps.CRUDS.users.serializers import UserSerializer
from apps.authentication.serializers import LogoutSerializer, LoginSerializer, RegisterSerializer, SetNewPasswordSerializer, ResetPasswordEmailRequestSerializer, UserTokenSerializer
from django.urls import reverse
from .utils import Util
from rest_framework.authtoken.models import Token
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
import jwt
from apps.authentication.models import User

class ProfileAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request,*args, **kwargs):
        token = request.GET.get('token')
        print(f'request -> {request.data}')
        print(f'El tken es -> {token}')
        try:
            token = Token.objects.filter(key = token).first()
            
            if token:
                user = token.user
                print(f'userr-> {user}')
                user_serializer = UserTokenSerializer(user)
            if user_serializer.is_valid():
                return Response({'user': user_serializer.data }, status = status.HTTP_200_OK)
            else:
                return Response({'error': user_serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'Token Invalido o expirado'}, status = status.HTTP_400_BAD_REQUEST)
        
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request):    
        users_serializer = self.serializer_class(data = request.data)
        if users_serializer.is_valid(): 
            users_serializer.save()
            user = User.objects.get(email=users_serializer.data['email'])
            tokens = user.tokens()

            # -- CONSTRUCCIÓN DEL CORREO --
            # Obtengo el dominio de donde se hace la request
            current_site = get_current_site(request).domain
            # Enlace de redireccionamiento para verificación
            relativeLink = reverse('verify_email')
            # URL absoluta para acceder desde el correo recibido
            absolute_urls = 'http://'+current_site+relativeLink+"?token="+str(tokens['access'])
            email_body = 'Hola, Bienvenido '+ user.username + '\nUsa este link para verificar tu registro. \n' + absolute_urls

            data = {'email_body': email_body, 'to_email': user.email,'email_subject': 'Verificación de cuenta'}
            res = Util.send_email(data)

            data_ = { "username": user.username, "email": user.email, 'name':user.name, "last_name":user.last_name, 'tokens': tokens}
            return Response({"message": "check your mailbox, we have sent a verification email", "user": data_}, status = status.HTTP_201_CREATED)
        
        return Response({"error": "unsuccessful user registration", "error": users_serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

class VerifyEmailAPIView(generics.GenericAPIView):
    
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user    = User.objects.get(id=payload['user_id'])
            
            # Activación del usuario (is_activate = True)
            if not user.is_activate:
                user.is_activate = True
                user.save()
            return Response({'email': "Successful account activation."}, status = status.HTTP_200_OK)
        
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activación expirada',"ERROR": identifier}, status = status.HTTP_400_BAD_REQUEST)     
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid or expired token'}, status = status.HTTP_400_BAD_REQUEST)     
        

class LoginAPIView(generics.GenericAPIView):
    
    def post(self, request):

        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            user_username = User.objects.filter(username = request.data['username'])
            try:
                user = User.objects.filter(username = request.data['username']).get()
            except:
                return Response({'error':'user not found, for username value'},status = status.HTTP_400_BAD_REQUEST)
            
            user_auth  = authenticate(email=user.email, password=serializer.validated_data['password'])
    
            if user_username.exists() and user_username[0].auth_provider != 'username':
                conflict = {'conflict': 'Continue with your login using ' + user_username[0].auth_provider}
                return Response({'conflict': conflict}, status = status.HTTP_409_CONFLICT)

            if not user_auth:
                return Response({'error':'password incorrect'}, status = status.HTTP_400_BAD_REQUEST)
                
            if not user_auth.is_active:
                return Response({'error': 'User blocked, contact the admin.'}, status = status.HTTP_400_BAD_REQUEST)

            data_ =  {
                'email': user_auth.email,
                'username': user_auth.username,
                'tokens': user_auth.tokens(),
                'auth_provider': user_auth.auth_provider
            }
            return Response({"message": "successful login", "user": data_}, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
            
                
class LogoutAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message":"successful logout."},status=status.HTTP_200_OK)
        
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
                return Response({'error':'No match found in email search, verify.'})
        else:
            return Response({'error': reset_serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'check your email, you were sent a link to reset your password.'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error':'Invalid token, request a new one'}, status=status.HTTP_400_BAD_REQUEST)
                
            return Response({'success':True,'message':'valid credentials', 'uidb64': uidb64,'token':token})
        
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)
         
class SetNewPasswordAPIView(generics.GenericAPIView):

    def patch(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message':'successful password reset.'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)