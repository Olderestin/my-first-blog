from django.urls import path
from .views import LoguotAPIView, RegisterView, VerifyEmail, LoginAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api-register'),
    path('email-verify/', VerifyEmail.as_view(), name='api-email-verify'),
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='api-token_refresh'),
    path('logout', LoguotAPIView.as_view(), name='api-logout')
]
