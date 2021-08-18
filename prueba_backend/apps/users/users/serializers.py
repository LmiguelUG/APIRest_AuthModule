from rest_framework import serializers
from apps.users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "name", "last_name", "email"]

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password']) # encriptación de contraseña al crear
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data) 
        user.set_password(validated_data['password']) # encriptación de contraseña al actualizar
        user.save()
        return user
        
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

    def to_representation(self, instance):
        return{
            'id': instance['id'],
            'username': instance['username'],
            'email': instance['email'],
            'name': instance['name'],
            'last_name': instance['last_name']
        }