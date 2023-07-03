from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
from .models import Address, Patient
# Create your views here.

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    is_superuser = forms.BooleanField(required=True)
    is_staff = forms.BooleanField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + \
        ('email', 'first_name', 'last_name', 'is_superuser', 'is_staff')

class UserRegistrationAPIView(APIView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        form = CustomUserCreationForm(request.data)
        if form.is_valid():
            user = form.save()
            return Response({'message': 'User registered successfully'})
        else:
            return Response(form.errors, status=400)

class UserLoginAPIView(APIView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            fields_to_include = ['username', 'email', 'first_name', 'last_name']
            user_dict = model_to_dict(user, fields=fields_to_include)
            return Response({'message': 'User logged in successfully', 'user': user_dict})

        return Response({'message': 'User logged in failed'})

class UserLogoutAPIView(APIView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        logout(request)
        return Response({'message': 'User logged out successfully'})
    
# patients view
class CreatePatientAPIView(APIView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        try:
            patient_data = request.data.get('patient', {})
            address_data = request.data.get('address', {})

            first_name = patient_data.get('first_name')
            middle_name = patient_data.get('middle_name')
            last_name = patient_data.get('last_name')
            contact_email = patient_data.get('contact_email')
            contact_phone = patient_data.get('contact_phone')
            date_of_birth = patient_data.get('date_of_birth')
            height = patient_data.get('height')
            weight = patient_data.get('weigth')
            blood_group = patient_data.get('blood_group')

            address_1 = address_data.get('address_1')
            address_2 = address_data.get('address_2')
            address_3 = address_data.get('address_3')
            city = address_data.get('city')
            state = address_data.get('state')
            postal_code = address_data.get('postal_code')
            country = address_data.get('country')

            address_data = {
                'address_1': address_1,
                'address_2': address_2,
                'address_3': address_3,
                'city': city,
                'state': state,
                'postal_code': postal_code,
                'country': country
            }

            if any(value for value in address_data.values()):
                # address data is not empty, check if address already exists
                existing_address = Address.objects.filter(**address_data).first()
                if existing_address:
                    address = existing_address
                else:
                    # create a new address object
                    address = Address.objects.create(**address_data)
                    address.save()
            else:
                # address data is empty, set the address foreign key to null
                address = None
            
            patient_data = {
                'first_name': first_name,
                'middle_name': middle_name,
                'last_name': last_name,
                'contact_email': contact_email,
                'contact_phone': contact_phone,
                'date_of_birth': date_of_birth,
                'height': height,
                'weight': weight,
                'blood_group': blood_group,
                'address': address
            }

            patient = Patient.objects.create(**patient_data)
            patient.save()

            return Response({'message': 'Patient created successfully'})
        except Exception as e:
            return Response({'message': 'Error', 'error': str(e)}, status=500)
        
