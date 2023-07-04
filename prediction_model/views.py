from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import Patient, DiabetesAnalysis
import numpy as np
import joblib

class ModelDiabetesPrediction(APIView):

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        # extract and preprocess input data
        # patient_data = request.data.get('patient')
        diabetes_data = request.data.get('data')

        preprocessed_data = preprocess_data(diabetes_data)
        # load the trained model
        model = joblib.load('./ml_model/diabetes_model.pk1')

        try:
            # make predictions
            prediction = model.predict(preprocessed_data)

            # create diabetesanalysis object with prediction
            # diabetes_analysis = DiabetesAnalysis.objects.create(data)
            
            return Response({"message": str(prediction)})
        except Exception as e:
            return Response({'error': str(e)}, status=500)

def preprocess_data(data):
    glucose = data['glucose']
    blood_pressure = data['blood_pressure']
    insulin = data['insulin']
    bmi = data['bmi']
    diabetes_func = data['diabetes_func']
    age = data['age']

    array_2d = np.array([[glucose, blood_pressure, insulin, bmi, diabetes_func, age]])

    array_2d = array_2d.reshape((1,-1))

    return array_2d

