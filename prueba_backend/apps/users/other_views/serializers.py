from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from apps.users.models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class LoginSerializer(serializers.ModelSerializer):
    email    = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, write_only=True) #read_only
    tokens   = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(username = obj['username'])

        return {'refresh': user.tokens()['refresh'],'access': user.tokens()['access']}

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email    = attrs.get('email', '')
        password = attrs.get('password', '')
        username = attrs.get('username', '')

        user_username = User.objects.filter(username = username)
        user_auth = authenticate(email=email, password=password)
        
        if user_username.exists() and user_username[0].auth_provider != 'username':
            raise AuthenticationFailed(
                detail='Continúe con su inicio de sesión usando ' + user_username[0].auth_provider)

        if not user_auth:
            raise AuthenticationFailed('Contraseña Incorrecta.')
        if not user_auth.is_active:
            raise AuthenticationFailed('Usuario bloqueado, contacte al admin')

        return {'email': user_auth.email,'username': user_auth.username,'is_activate': user_auth.is_activate,'tokens': user_auth.tokens()}
        return super().validate(attrs)


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