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
        patient_data = request.data.get('patient')
        diabetes_data = request.data.get('data')

        preprocessed_data = preprocess_data(
            diabetes_data, patient_data.get('id'))
        # load the trained model
        model = joblib.load('./ml_model/diabetes_model.pk1')

        try:
            # check if diabetes analysis already exists for the patient ID
            if DiabetesAnalysis.objects.filter(patient_id=patient_data.get('id')).exists():
                return Response({"message": "Diabetes analysis already exists for this patient"})

            # make predictions
            prediction = model.predict(preprocessed_data)
            outcome = int(prediction[0])

            # prepare data

            analysis_data = {
                'glucose': diabetes_data.get('glucose'),
                'blood_pressure': diabetes_data.get('blood_pressure'),
                'insulin': diabetes_data.get('insulin'),
                'bmi': diabetes_data.get('bmi'),
                'patient_id': patient_data.get('id'),
                'outcome': outcome
            }
            # create diabetesanalysis object with prediction
            analysis = DiabetesAnalysis.objects.create(**analysis_data)
            analysis.save()

            return Response({"message": "Analysis successful"})
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    def put(self, request, analysis_id):
        try:
            analysis = DiabetesAnalysis.objects.get(id=analysis_id)
            preprocessed_data = preprocess_data(
                request.data, analysis.patient.id)

            # load the trained model
            model = joblib.load('./ml_model/diabetes_model.pk1')
            # make predictions
            prediction = model.predict(preprocessed_data)
            outcome = int(prediction[0])

            data = request.data
            analysis.glucose = data.get('glucose', analysis.glucose)
            analysis.blood_pressure = data.get(
                'blood_pressure', analysis.blood_pressure)
            analysis.insulin = data.get('insulin', analysis.insulin)
            analysis.bmi = data.get('bmi', analysis.bmi)
            analysis.outcome = outcome

            analysis.save()

            return Response({"message": "Diabetes analysis update successfully"})
        except DiabetesAnalysis.DoesNotExist:
            return Response({"message": "Diabetes analysis not found"}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


def preprocess_data(data, patient_id):
    patient = Patient.objects.get(id=patient_id)
    glucose = data['glucose']
    blood_pressure = data['blood_pressure']
    insulin = data['insulin']
    bmi = data['bmi']
    age = patient.age

    array_2d = np.array([[glucose, blood_pressure, insulin, bmi, age]])

    array_2d = array_2d.reshape((1, -1))

    return array_2d
