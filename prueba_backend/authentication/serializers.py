from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from authentication.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError

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

class ProfileSerializer(serializers.ModelSerializer):

   class Meta:
        model = User
        fields = ("username", "email")
    

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length = 80, min_length = 8, write_only = True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length = 80, min_length = 8, write_only = True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'token')
        read_only_fields = ['token', 'email']
                
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_message = {'bad_token': ('Invalid or expired token.')}

    def validate(self, validated_data):
        self.token = validated_data['refresh']
        return validated_data

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except:
            return f'Token errado.'