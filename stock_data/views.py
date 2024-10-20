import joblib
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from datetime import datetime, timedelta

class PredictStockPriceView(APIView):
    def get(self, request):
        model = joblib.load('stock_data/ml_models/linear_regression_model.pkl')

        future_dates = [datetime.now().date() + timedelta(days=i) for i in range(1, 31)]
        day_of_year = [date.timetuple().tm_yday for date in future_dates]
        X_future = pd.DataFrame({'day': day_of_year})

        # Make predictions
        predictions = model.predict(X_future)


        # Prepare response
        prediction_results = {
            'dates': [date.strftime('%Y-%m-%d') for date in future_dates],
            'predicted_prices': predictions.tolist(),
        }

        return Response(prediction_results, status=status.HTTP_200_OK)
