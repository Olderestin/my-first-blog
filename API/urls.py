from django.urls import path
from .views import LoguotAPIView, RegisterView, VerifyEmail, LoginAPIView, RequestPasswordResetEmail, PasswordTokenCheckAPI
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api-register'),
    path('email-verify/', VerifyEmail.as_view(), name='api-email-verify'),
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='api-token-refresh'),
    path('logout', LoguotAPIView.as_view(), name='api-logout'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name='api-request-reset-email'),
    path('password-reset/<uid64>/<token>/', PasswordTokenCheckAPI.as_view(), name='api-password-reset-confirm')
]
