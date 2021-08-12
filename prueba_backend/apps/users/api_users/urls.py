from django.urls import path
from apps.users.api_users.api import user_api_view, user_detail_api_view

urlpatterns = [
    path('', user_api_view, name = 'user_view'),
    path('<int:pk>', user_detail_api_view, name = 'user_detail_view')
]