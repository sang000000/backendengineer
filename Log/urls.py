from django.urls import path
from . import views
from .views import CustomTokenRefreshView

app_name = "accounts"
urlpatterns = [
    path("signup/", views.signup.as_view(), name="signup"),
    path("login/", views.Login.as_view(), name="Login"),
    path("accessverification/", views.AccessVerification.as_view(), name="accessverification"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]