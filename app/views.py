from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate, login, logout
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
            return Response(form.erros, status=400)

class UserLoginAPIView(APIView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'message': 'User logged in successfully'})

        return Response({'message': 'User logged in successfully'})

class UserLogoutAPIView(APIView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        logout(request)
        return({'message': 'User logged out successfully'})
