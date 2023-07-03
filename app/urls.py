from django.urls import path
from .views import CustomUserCreationForm, UserRegistrationAPIView, UserLoginAPIView, UserLogoutAPIView, CreatePatientAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('logout/', UserLogoutAPIView.as_view(), name='user-logout'),
    path('patients/create/', CreatePatientAPIView.as_view(), name='create-patient')
]