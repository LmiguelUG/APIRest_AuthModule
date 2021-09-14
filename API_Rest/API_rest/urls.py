from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # CRUD'S
    path('api/user/', include('cruds.users.urls')), # Path for user CRUD
    path('api/permission/', include('cruds.permissions.urls')), # Path for permissions CRUD
    
    # Authentication username
    path('api/auth/', include('authentication.urls')),
       
    # Authentificación social (facebook - google)
    path('api/auth/social/', include('socialauthentication.urls')), 
]
