from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from authentication.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length = 80, min_length = 8, write_only = True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length = 80, min_length = 8, write_only = True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(username = obj.username)
        return { 'refresh': user.tokens()['refresh'], 'access': user.tokens()['access'] }

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'tokens')

    def validate(self, data):
        username = data.get('username','')
        password = data.get('password','')
        user = auth.authenticate(username=username,password=password)
        
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        
        return {'email': user.email, 'username': user.username, 'tokens': user.tokens }


class ProfileSerializer(serializers.ModelSerializer):

   class Meta:
        model = User
        fields = ("username", "email")


class LogoutSerializer(serializers.ModelSerializer):
    
    refresh = serializers.CharField()
    
    class Meta:
        model = User
        fields = ['refresh']

    def validate(self, data):
        self.token = data['refresh']
        return data

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except:
             return Response({'message': 'token invalid'}, status = status.HTTP_401_UNAUTHORIZED)  




class UserTokenSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    
    class Meta:
        fields = ['email']

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, validated_data):
        try:
            password = validated_data.get('password')
            token    = validated_data.get('token')
            uidb64   = validated_data.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Invalid reset link '}, status = status.HTTP_401_UNAUTHORIZED)
            
            # Establecimiento de contraseña(nueva) a usuario
            user.set_password(password)
            user.save()
            return (user)
            
        except Exception as e:
             return Response({'message': 'Link de reestablecimiento invalido'}, status = status.HTTP_401_UNAUTHORIZED)
        return super().validate(validated_data)

                
