from rest_framework import serializers
from django.contrib.auth.models import Permission

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission        
        fields= '__all__'

        # def create(self, validated_data):
        #     permission = Permission(**validated_data)
        #     permission.save()
        #     return permission

        def update(self, instance, validated_data):
            permission = super().update(instance, validated_data) 
            permission.save()
            return permission

class UpdatePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields= []

        def to_representation(self, instance):
            return{
                'id': instance['id'],
                'name': instance['name'],
                'codename': instance['codename'],
                'content_type': instance['content_type']
            }
        
class PermissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission

    def to_representation(self, instance):
        return{
            'id': instance['id'],
            'name': instance['name'],
            'codename': instance['codename'],
            'content_type': instance['content_type']
        }