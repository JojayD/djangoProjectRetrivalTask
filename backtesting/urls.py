from django.urls import path
from .views import BacktestView ,ReportView

urlpatterns = [
    path('run/', BacktestView.as_view(), name='backtest'),
    path('report/', ReportView.as_view(), name='report'),
]