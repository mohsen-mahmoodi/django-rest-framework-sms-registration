from django.urls import re_path, include, path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

auth_urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='auth-register'),
    path('verify/', views.VerificationView.as_view(), name='auth-verify'),
    path('profile/', views.ProfileView.as_view(), name='auth-profile'),
    path('password/', views.PasswordView.as_view(), name='auth-password'),

    path('token/', views.TokenObtainPairView.as_view(), name='auth-token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='auth-token-refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='auth-token-verify'),

]


urlpatterns = [
    path('auth/', include(auth_urlpatterns)),
    path('services/', views.ServiceView.as_view(), name='services')
]
