from django.contrib import admin
from django.urls import path, include
from apps.authentication.views import LoginAPIView, LogoutAPIView, RegisterView, PasswordTokenCheckAPI,VerifyEmailAPIView, RequestPasswordResetEmail, ProfileAPIView, SetNewPasswordAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # CRUD'S
    path('api/user/', include('apps.CRUDS.users.urls')), # Path for user CRUD
    path('api/rol/', include('apps.CRUDS.roles.urls')), # Path for user role CRUD
    path('api/permission/', include('apps.CRUDS.permissions.urls')), # Path for permissions CRUD
    
    # Authentication
    path('login', LoginAPIView.as_view(), name = 'login'),
    path('logout', LogoutAPIView.as_view(), name = 'logout'),
    path('register', RegisterView.as_view(), name='register'),
    # verificación por correo para activacion de cuenta (is_activate = True)
    path('verify_email/', VerifyEmailAPIView.as_view(), name='verify_email'),
    path('profile', ProfileAPIView.as_view(), name = 'profile'),

    # Reestablecimietno de contraseña
    path('reset_password', RequestPasswordResetEmail.as_view(), name='reset_password'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password_reset_confirm'),
    path('password_reset_complete', SetNewPasswordAPIView.as_view(), name='password_reset_complete'), 
    
    # Authentificación social (facebook - google)
    path('accounts/', include('apps.socialauthentication.urls'), name='account_google'), 
]

# {
#     "success": true,
#     "message": "credenciales validas",
#     "uidb64": "MTQ",
#     "token": "arjz0f-eb64cf043eebf337c7a529699c5505c0"
# }
