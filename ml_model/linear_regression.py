from sklearn.linear_model import LinearRegression
import pandas as pd
import joblib
from stock_data.models import StockPrice

# Fetch data
data = pd.DataFrame.from_records(
    StockPrice.objects.filter(symbol='AAPL').order_by('date').values('date', 'close_price')
)
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)

# Prepare features
data['day'] = data.index.dayofyear
X = data[['day']]
y = data['close_price']

# Train model
model = LinearRegression()
model.fit(X, y)

# Save the model
joblib.dump(model, 'stock_data/ml_models/linear_regression_model.pkl')
