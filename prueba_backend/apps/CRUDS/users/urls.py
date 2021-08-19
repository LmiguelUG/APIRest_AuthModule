from django.urls import path
from apps.CRUDS.users.api import UserAPI, UserDetailsAPI

urlpatterns = [
    path('', UserAPI, name = 'UserAPI'),
    path('<int:pk>/', UserDetailsAPI, name = 'UserDetailsAPI')
]