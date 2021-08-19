from django.urls import path
from apps.socialauthentication.views import GoogleAPIView, FacebookAPIView

urlpatterns = [
    path('google/', GoogleAPIView.as_view(), name='GoogleAPIView'),

    # Primero
    path('facebook/', FacebookAPIView.as_view(), name='FacebookAPIView'),
]