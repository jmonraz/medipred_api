from django.urls import path
from .views import CustomUserCreationForm, UserRegistrationAPIView, UserLoginAPIView, UserLogoutAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('logout/', UserLogoutAPIView.as_view(), name='user-logout')
]