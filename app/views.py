from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
from .models import Address, Patient, DiabetesAnalysis
from datetime import date, datetime
from django.core.exceptions import ValidationError
from django.core import serializers
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
            fields_to_include = ['username',
                                 'email', 'first_name', 'last_name']
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
            contact_email = patient_data.get('contact_email')

            # Check if a user with the same contact_email already exists
            if Patient.objects.filter(contact_email=contact_email).exists():
                raise ValidationError({'contact_email':
                                       'A user with the same email already exists.'})

            first_name = patient_data.get('first_name')
            middle_name = patient_data.get('middle_name')
            last_name = patient_data.get('last_name')
            contact_email = patient_data.get('contact_email')
            contact_phone = patient_data.get('contact_phone')
            date_of_birth = patient_data.get('date_of_birth')
            dob = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
            age = calculate_age(dob)
            gender = patient_data.get('gender')
            height = patient_data.get('height')
            weight = patient_data.get('weight')
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
                existing_address = Address.objects.filter(
                    **address_data).first()
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
                'age': age,
                'gender': gender,
                'address': address
            }

            patient = Patient.objects.create(**patient_data)
            patient.save()

            return Response({'message': 'Patient created successfully'})
        except ValidationError as e:
            return Response({'message': 'Error', 'error': dict(e)}, status=400)
        except Exception as e:
            return Response({'message': 'Error', 'error': str(e)}, status=500)

    def put(self, request, patient_id):
        try:
            patient = Patient.objects.get(id=patient_id)

            data = request.data.get('patient', {})
            patient.first_name = data.get('first_name', patient.first_name)
            patient.middle_name = data.get('middle_name', patient.middle_name)
            patient.last_name = data.get('last_name', patient.last_name)
            patient.contact_email = data.get(
                'contact_email', patient.contact_email)
            patient.contact_phone = data.get(
                'contact_phone', patient.contact_phone)
            patient.height = data.get('height', patient.height)
            patient.weight = data.get('weight', patient.weight)
            patient.blood_group = data.get('blood_group', patient.blood_group)
            patient.enabled = data.get('enabled', patient.enabled)

            data = request.data.get('address', {})
            address_data = {
                'address_1': data.get('address_1'),
                'address_2': data.get('address_2'),
                'address_3': data.get('address_3'),
                'city': data.get('city'),
                'state': data.get('state'),
                'postal_code': data.get('postal_code'),
                'country': data.get('country'),
            }

            if any(value for value in address_data.values()):
                # address data is not empty, check if address already exists
                existing_address = Address.objects.filter(
                    **address_data).first()
                if existing_address:
                    patient.address = existing_address
                else:
                    # create a new address object
                    address = Address.objects.create(**address_data)
                    address.save()
                    patient.address = address
            else:
                # address data is empty, set the address foreign key to null
                address = None

            patient.save()

            return Response({'message': 'patient updated'})
        except Exception as e:
            return Response({'error', str(e)}, status=400)


class GetAllPatients(APIView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        patients = Patient.objects.all()
        patient_list = []
        for patient in patients:

            patient_data = {
                'id': patient.id,
                'first_name': patient.first_name,
                'middle_name': patient.middle_name,
                'last_name': patient.last_name,
                'contact_email': patient.contact_email,
                'contact_phone': patient.contact_phone,
                'date_of_birth': patient.date_of_birth,
                'height': patient.height,
                'weight': patient.weight,
                'blood_group': patient.blood_group,
                'age': patient.age,
                'gender': patient.gender,
                'enabled': patient.enabled,
            }
            if patient.address is not None:
                patient_data['address'] = patient.address.id
            else:
                patient_data['address'] = None
            patient_list.append(patient_data)
        return Response({'patients': patient_list})


class GetDiabetesAnalysis(APIView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        analysis = DiabetesAnalysis.objects.all()
        analysis_list = []

        for a in analysis:
            formatted_datetime = a.last_checked.strftime('%Y-%m-%d %H:%M:%S')
            analysis_data = {
                'analysis_id': a.id,
                'id': a.patient.id,
                'first_name': a.patient.first_name,
                'last_name': a.patient.last_name,
                'gender': a.patient.gender,
                'age': a.patient.age,
                'glucose': a.glucose,
                'blood_pressure': a.blood_pressure,
                'insulin': a.insulin,
                'bmi': a.bmi,
                'outcome': a.outcome,
                'last_checked': formatted_datetime,
            }
            analysis_list.append(analysis_data)
        return Response({"data": analysis_list})


class GetAddressById(APIView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, address_id):
        try:
            address = Address.objects.get(id=address_id)
            address_data = {
                'id': address.id,
                'address_1': address.address_1,
                'address_2': address.address_2,
                'address_3': address.address_3,
                'city': address.city,
                'state': address.state,
                'postal_code': address.postal_code,
                'country': address.country
            }
            return Response({"data": address_data})
        except Exception as e:
            return Response({"error": str(e)}, status=400)


def calculate_age(date_of_birth):
    today = date.today()
    age = today.year - date_of_birth.year

    # check if the birthday has already occurred this year
    if today.month < date_of_birth.month or (today.month == date_of_birth.month) and today.day < date_of_birth.day:
        age -= 1

    return age
