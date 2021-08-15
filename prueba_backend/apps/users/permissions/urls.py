from django.urls import path
from apps.users.permissions.api import permissions_api_view, permission_detail_api_view

urlpatterns = [
    path('', permissions_api_view, name = 'permissions_view'),
    path('<int:pk>', permission_detail_api_view, name = 'permission_detail_view')
]