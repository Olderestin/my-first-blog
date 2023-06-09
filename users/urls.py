from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('profile/<username>', views.profile, name='profile'),
    path('password_change', views.password_change, name='password_change'),
    path('password_reset', views.password_reset_request, name='password_reset'),
    path('reset/<uidb64>/<token>', views.PasswordResetConfirm, name='password_reset_confirm'),
    path('social/signup/', views.signup_redirect, name='signup_redirect'),
]