from django.urls import path
from socialauthentication.views import GoogleAPIView, FacebookAPIView

urlpatterns = [
    path('google/', GoogleAPIView.as_view(), name='GoogleAPIView'),
    path('facebook/', FacebookAPIView.as_view(), name='FacebookAPIView'),
]