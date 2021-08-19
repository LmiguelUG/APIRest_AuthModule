from django.contrib.contenttypes.models import ContentType
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.CRUDS.permissions.serializers import PermissionSerializer, PermissionListSerializer, UpdatePermissionSerializer

# Importacion de modelos
from django.contrib.auth.models import Permission
from apps.authentication.models import User
from apps.authentication.models import Rol



@api_view(['GET', 'POST'])
def PermissionAPI(request):
 
    # List, List all existing permissions by default in django in the Permission model
    if request.method == 'GET': 
        permissions = Permission.objects.all().values('id', 'name','content_type','codename')
        permissions_serializer = PermissionListSerializer(permissions, many = True)
        return Response(permissions_serializer.data, status = status.HTTP_200_OK)

    # Create
    if request.method == 'POST':
        if request.data:

            # Planteamiento del tipo de contenido (content_type)
            if 'content' in request.data:

                content = request.data['content'].lower()
                if content == 'user':
                    ct = ContentType.objects.get_by_natural_key('authentication', 'user')          
                elif content == 'rol':
                    ct = ContentType.objects.get_for_model(Rol)           
                else:
                    return Response({'error': 'The nonexistent content type'}, status = status.HTTP_409_CONFLICT)
            else:
                return Response({'error':"missing 'content' value."}, status = status.HTTP_400_BAD_REQUEST)
            
            # Planteamiento del nombre del permiso (name)
            if 'action' in request.data:
                if content == 'user':
                    name = f"Can {request.data['action']} user"

                if content == 'rol':
                    name = f"can {request.data['action']} rol"
                
                # Planteamiento del codigo del permiso (codename)
                codename = request.data['action'].lower()
            else:
                return Response({'error':"missing 'action' value."}, status = status.HTTP_400_BAD_REQUEST)
                      
            # Creación del permiso
            permission = Permission.objects.update_or_create(content_type = ct,codename = codename,name = name)
            if permission:
                return Response({'message':'Permission created successfully.'}, status = status.HTTP_201_CREATED)
            else:
                return Response({'error':'permission creation not successful'}, status = status.HTTP_409_CONFLICT)          
        else:
            return Response({'error':'Missing data.'}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def PermissionDetailsAPI(request,pk=None):
    
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
                        ct = ContentType.objects.get_by_natural_key('authentication', 'user')          
                    elif content == 'rol':
                        ct = ContentType.objects.get_for_model(Rol)           
                    else:
                        return Response({'error': 'The nonexistent content type'}, status = status.HTTP_409_CONFLICT)
                else:
                    return Response({'error':"missing 'content' data."}, status = status.HTTP_400_BAD_REQUEST)

                # Planteamiento del nombre del permiso (name)
                if 'action' in request.data:
                    if content == 'user':
                        name = f"Can {request.data['action']} user"
                    if content == 'rol':
                        name = f"can {request.data['action']} rol" 
                    # Planteamiento del codigo del permiso (codename)
                    codename = request.data['action'].lower()
                else:
                    return Response({'error':"missing 'action' data."}, status = status.HTTP_400_BAD_REQUEST)
                      
                # Actualización del permiso
                permission = Permission.objects.filter(id=pk).update(content_type = ct,codename = codename,name = name)
                if permission:
                    return Response({'message':'Permission updated successfully.'}, status = status.HTTP_201_CREATED)
                else:
                    return Response({'error':'permission update unsuccessful'}, status = status.HTTP_409_CONFLICT)          
            else:
                return Response({'error':'Missing data'}, status = status.HTTP_400_BAD_REQUEST)
        
        # Delete
        elif request.method == 'DELETE':
            permission.delete()
            message = f'permission removed successfully.'
            return Response({"message": message, 'permission deleted': permission.name}, status = status.HTTP_200_OK)

    return Response({'error:': 'Permission not found, check the data'}, status = status.HTTP_400_BAD_REQUEST)