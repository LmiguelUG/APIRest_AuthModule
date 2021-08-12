from django.urls import path
from apps.users.api_roles.api import roles_api_view, rol_detail_api_view

urlpatterns = [
    path("", roles_api_view, name = 'roles_view'),
    path("<int:pk>", rol_detail_api_view, name = 'roles_details_view')
]