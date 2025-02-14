from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

app_name = "accounts"
urlpatterns = [
    path("signup/", views.signup.as_view(), name="signup"),
    path("login/", views.Login.as_view(), name="Login"),
    path("accessverification/", views.AccessVerification.as_view(), name="accessverification"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]