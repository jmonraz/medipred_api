from django.urls import path
from .views import ModelDiabetesPrediction

urlpatterns = [
    path('diabetes/predict/', ModelDiabetesPrediction.as_view(), name='diabetes-prediction'),
]