from django.contrib import admin
from django.urls import path, include
from apps.users.other_views.views import Login, LogoutAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('apps.users.users.urls')), # Path for user CRUD
    path('rol/', include('apps.users.roles.urls')), # Path for user role CRUD
    path('permission/', include('apps.users.permissions.urls')), # Path for permissions CRUD
    
    path('login/', Login.as_view(), name = 'login'),
    path('logout/', LogoutAPIView.as_view(), name = 'logout'),
    path('register/', include('apps.users.users.urls'), name='register')
]
