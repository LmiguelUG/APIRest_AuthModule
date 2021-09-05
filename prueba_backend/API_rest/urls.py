from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # CRUD'S
    path('api/user/', include('apps.CRUDS.users.urls')), # Path for user CRUD
    path('api/rol/', include('apps.CRUDS.roles.urls')), # Path for user role CRUD
    path('api/permission/', include('apps.CRUDS.permissions.urls')), # Path for permissions CRUD
    
    # Authentication username
    path('api/auth/', include('authentication.urls')),
       
    # Authentificación social (facebook - google)
    path('api/auth/social/', include('socialauthentication.urls')), 
]
