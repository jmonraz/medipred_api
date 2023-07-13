from django.urls import path
from .views import CustomUserCreationForm, UserRegistrationAPIView, \
    UserLoginAPIView, UserLogoutAPIView, CreatePatientAPIView, GetAllPatients, GetDiabetesAnalysis, GetAddressById

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('logout/', UserLogoutAPIView.as_view(), name='user-logout'),
    path('patients/create/', CreatePatientAPIView.as_view(), name='create-patient'),
    path('patients/edit/<int:patient_id>/',
         CreatePatientAPIView.as_view(), name='edit-patient'),
    path('patients/', GetAllPatients.as_view(), name='get-patients'),
    path('diabetes/', GetDiabetesAnalysis.as_view(), name='get-diabetes'),
    path('address/<int:address_id>/',
         GetAddressById.as_view(), name='get-address'),
]
