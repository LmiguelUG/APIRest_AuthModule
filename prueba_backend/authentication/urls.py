from django.urls import path
from authentication.views import LoginAPIView, LogoutAPIView, RegisterView, PasswordTokenCheckAPI, VerifyEmailAPIView
from authentication.views import RequestPasswordResetEmail, ProfileAPIView, SetNewPasswordAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login', LoginAPIView.as_view(), name = 'login'),
    path('logout', LogoutAPIView.as_view(), name = 'logout'),
    path('register', RegisterView.as_view(), name='register'),
    path('verify_email/', VerifyEmailAPIView.as_view(), name='verify_email'), # verificación por correo para activacion de cuenta (is_activate = True)
    path('profile', ProfileAPIView.as_view(), name = 'profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Reestablecimietno de contraseña
    path('reset_password', RequestPasswordResetEmail.as_view(), name='reset_password'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password_reset_confirm'),
    path('password_reset_complete', SetNewPasswordAPIView.as_view(), name='password_reset_complete'), 
]