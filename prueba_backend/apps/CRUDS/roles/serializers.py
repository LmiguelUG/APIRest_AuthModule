from rest_framework import serializers
from apps.CRUDS.roles.models import Rol

class RolSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rol
        fields = '__all__'
    
    def create(self,validated_data):
        rol = Rol(**validated_data)
        rol.save()
        return rol

    def update(self, instance, validated_data):
        rol = super().update(instance, validated_data)
        rol.save()
        return rol
