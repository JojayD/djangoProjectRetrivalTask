from django.urls import path
from backtesting import views
from stock_data.views import PredictStockPriceView

urlpatterns = [
    # ...
    path('predict/', PredictStockPriceView.as_view(), name='predict'),
]
