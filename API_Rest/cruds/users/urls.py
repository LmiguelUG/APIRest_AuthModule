from django.urls import path
from cruds.users.api import UserAPI, UserDetailsAPI

urlpatterns = [
    path('', UserAPI, name = 'UserAPI'),
    path('<int:pk>/', UserDetailsAPI, name = 'UserDetailsAPI'),
]