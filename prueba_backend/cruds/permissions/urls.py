from django.urls import path
from apps.CRUDS.permissions.api import PermissionAPI, PermissionDetailsAPI

urlpatterns = [
    path('', PermissionAPI, name = 'PermissionAPI'),
    path('<int:pk>', PermissionDetailsAPI, name = 'PermissionDetailsAPI')
]