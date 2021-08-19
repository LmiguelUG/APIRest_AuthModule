from django.urls import path
from apps.CRUDS.roles.api import RolAPI, RolDetailAPI

urlpatterns = [
    path("", RolAPI, name = 'RolAPI'),
    path("<int:pk>", RolDetailAPI, name = 'RolDetailAPI')
]