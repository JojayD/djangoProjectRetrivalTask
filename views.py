# In djangoProjectRetrivalTask/views.py
from django.shortcuts import redirect

def home(request):
    return redirect('backtest')  # Assumes 'backtest' is the name of your backtesting URL