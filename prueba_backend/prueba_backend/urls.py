from django.contrib import admin
from django.urls import path, include
from apps.users.other_views.views import LoginAPIView, LogoutAPIView, RegisterView, PasswordTokenCheckAPI,VerifyEmailAPIView, RequestPasswordResetEmail, SetNewPasswordAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # CRUD'S
    path('api/user', include('apps.users.users.urls')), # Path for user CRUD
    path('rol/', include('apps.users.roles.urls')), # Path for user role CRUD
    path('permission/', include('apps.users.permissions.urls')), # Path for permissions CRUD
    
    # Vistas asociadas
    path('login/', LoginAPIView.as_view(), name = 'login'),
    path('logout/', LogoutAPIView.as_view(), name = 'logout'),
    path('register/', RegisterView.as_view(), name='register'),

    # verificación por correo de registro
    path('verify_email/', VerifyEmailAPIView.as_view(), name='verify_email'),

    # Reestablecimietno de contraseña
    path('reset_password/', RequestPasswordResetEmail.as_view(), name='reset_password'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', SetNewPasswordAPIView.as_view(), name='password_reset_complete'), 
    
    # Authentificación social (facebook - google)
    path('accounts/', include('apps.authsocial.urls'), name='account_google'), 
]

# {
#     "success": true,
#     "message": "credenciales validas",
#     "uidb64": "MTQ",
#     "token": "arjz0f-eb64cf043eebf337c7a529699c5505c0"
# }
