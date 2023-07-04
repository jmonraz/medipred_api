from rest_framework.response import Response
from rest_framework.views import APIView
import joblib

class ModelPrediction(APIView):

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        # extract and preprocess input data
        input_data = request.data
        preprocessed_data = preprocess_data(input_data)
        # load the trained model
        model = joblib.load('./ml_model/diabetes_model.pk1')

        try:
            # make predictions
            prediction = model.predict(preprocessed_data)

            # format the response
            response = {
                'prediction': prediction
            }

            return Response(response)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

def preprocess_data():
    return 1

def predict():
    return 2
