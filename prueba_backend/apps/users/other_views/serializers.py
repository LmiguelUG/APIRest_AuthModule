from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from apps.users.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "name", "last_name", "email", "password"]

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password']) # encriptación de contraseña al crear
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    email    = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField (max_length=68,  min_length=6, write_only=True)
    username = serializers.CharField (max_length=255, min_length=3, write_only=True)
    tokens   = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user   = User.objects.get(username = obj['username'])
        tokens = user.tokens()
        return tokens

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, validated_data):
        email    = validated_data.get('email','')
        password = validated_data.get('password','')
        username = validated_data.get('username','')  
    
        return validated_data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_message = {'bad_token': ('Token invalido o expirado.')}

    def validate(self, validated_data):
        self.token = validated_data['refresh']
        return validated_data

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except:
            return f'Token errado.'