from django.urls import path

from .views import *

urlpatterns = [
    path("login", LoginAPIView.as_view(), name="inico de sesion"),
    path("register", RegisterAPIView.as_view(), name="registro de usuarios"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("profile/", ProfileAPIView.as_view(), name="profile"),
    path("verify-email/", VerifyEmailAPIView.as_view(), name="VerifyEmailAPIView"),
    path(
        "resend-verification/",
        ResendVerificationAPIView.as_view(),
        name="ResendVerificationAPIView",
    ),
    path(
        "password-reset/request/",
        RequestPasswordResetAPIView.as_view(),
        name="request-password-reset",
    ),
    path(
        "password-reset/verify/",
        VerifyPasswordResetCodeAPIView.as_view(),
        name="verify-password-reset-code",
    ),
    path(
        "password-reset/confirm/", ResetPasswordAPIView.as_view(), name="reset-password"
    ),
]
