from django.urls import path
from apps.authsocial.views import GoogleView, FacebookView

urlpatterns = [
    path('google/', GoogleView.as_view(), name='google'),

    # Primero
    # https://www.facebook.com/v7.0/dialog/oauth?client_id={FACEBOOK_APP_ID}&redirect_uri=http://localhost:8000/login/&state={%22{st=state123abc,ds=123456789}%22}&scope=email
    path('facebook/', FacebookView.as_view(), name='facebook'),
]