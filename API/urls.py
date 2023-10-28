from django.urls import path, include
from .views import LoguotAPIView, RegisterView, VerifyEmail, LoginAPIView, RequestPasswordResetEmail, PasswordTokenCheckAPI, SetNewPassword, PostViewSet, PostImageViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'post-images', PostImageViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api-register'),
    path('email-verify/', VerifyEmail.as_view(), name='api-email-verify'),
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='api-token-refresh'),
    path('logout', LoguotAPIView.as_view(), name='api-logout'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name='api-request-reset-email'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='api-password-reset-confirm'),
    path('password-reset-complete/', SetNewPassword.as_view(), name='api-password-reset-complete'),
    path('', include(router.urls))
]
