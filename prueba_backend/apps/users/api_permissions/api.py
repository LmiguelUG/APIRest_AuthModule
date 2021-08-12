from django.contrib.contenttypes.models import ContentType
from apps.users.api_permissions.serializers import PermissionSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.api_permissions.serializers import PermissionSerializer, PermissionListSerializer, UpdatePermissionSerializer
# Importacion de modelos
from django.contrib.auth.models import Permission
from apps.users.models import User
from apps.users.models import Rol



@api_view(['GET', 'POST'])
def permissions_api_view(request):
 
    # List, List all existing permissions by default in django in the Permission model
    if request.method == 'GET': 
        permissions = Permission.objects.all().values('id', 'name','content_type','codename')
        permissions_serializer = PermissionListSerializer(permissions, many = True)
        return Response(permissions_serializer.data, status = status.HTTP_200_OK)

    # Create
    if request.method == 'POST':
        if request.data:
            if 'content' in request.data:
                content = request.data['content'].lower()
                if content == 'user':
                    ct = ContentType.objects.get_by_natural_key('users', 'user')          
                elif content == 'rol':
                    ct = ContentType.objects.get_for_model(Rol)           
                else:
                    return Response({'message': 'El tipo de contenido inexistente'}, status = status.HTTP_409_CONFLICT)
            else:
                return Response({'message':"error, dato 'content' faltante."}, status = status.HTTP_400_BAD_REQUEST)
            
            if 'action' in request.data:
                if content == 'user':
                    name = f"Can {request.data['action']} user"

                if content == 'rol':
                    name = f"can {request.data['action']} rol"
                
                codename = request.data['action'].lower()

            else:
                return Response({'message':"error, dato 'action' faltante."}, status = status.HTTP_400_BAD_REQUEST)
                      
            # permission creation
            permission = Permission.objects.update_or_create(content_type = ct,codename = codename,name = name)
            if permission:
                return Response({'message':'Permiso creado correctamente.'}, status = status.HTTP_201_CREATED)
            else:
                return Response({'message':'Error al intentar crear permiso.'}, status = status.HTTP_409_CONFLICT)          
        else:
            return Response({'message':'error, datos faltante.'}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def permission_detail_api_view(request,pk=None):
    
    permission = Permission.objects.filter(id=pk).first()
    if permission:

        # Retrieve
        if request.method == 'GET':
            permissions_serializer = PermissionSerializer(permission)
            return Response(permissions_serializer.data, status = status.HTTP_200_OK)
        
        # Update
        elif request.method == 'PUT':
            if request.data:
                if 'content' in request.data:
                    content = request.data['content'].lower()
                    if content == 'user':
                        ct = ContentType.objects.get_by_natural_key('users', 'user')          
                    elif content == 'rol':
                        ct = ContentType.objects.get_for_model(Rol)           
                    else:
                        return Response({'message': 'El tipo de contenido inexistente'}, status = status.HTTP_409_CONFLICT)
                else:
                    return Response({'message':"error, dato 'content' faltante."}, status = status.HTTP_400_BAD_REQUEST)
            
                if 'action' in request.data:
                    if content == 'user':
                        name = f"Can {request.data['action']} user"

                    if content == 'rol':
                        name = f"can {request.data['action']} rol"
                    
                    codename = request.data['action'].lower()
                else:
                    return Response({'message':"error, dato 'action' faltante."}, status = status.HTTP_400_BAD_REQUEST)
                      
                # permit update
                permission = Permission.objects.filter(id=pk).update(content_type = ct,codename = codename,name = name)
                if permission:
                    return Response({'message':'Permiso actualizado correctamente.'}, status = status.HTTP_201_CREATED)
                else:
                    return Response({'message':'Error al intentar actualizar permiso.'}, status = status.HTTP_409_CONFLICT)          
            else:
                return Response({'message':'error, datos faltante.'}, status = status.HTTP_400_BAD_REQUEST)
        
        # Delete
        elif request.method == 'DELETE':
            permission.delete()
            message = f'permiso eliminado exitosamente.'
            return Response({"message": message, 'permission deleted': permission.name}, status = status.HTTP_200_OK)

    return Response({'message:': 'Permiso no encontrado, verifica los datos'}, status = status.HTTP_400_BAD_REQUEST)