from django.urls import path
from .views import RegisterView, VerifyEmail

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api-register'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify')
]
