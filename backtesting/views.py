from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny
from stock_data.models import StockPrice
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use 'Agg' backend for server environments
import matplotlib.pyplot as plt
from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

class BacktestSerializer(serializers.Serializer):
    initial_investment = serializers.FloatField(default=10000)
    short_window = serializers.IntegerField(default=50)
    long_window = serializers.IntegerField(default=200)

    def validate(self, data):
        if data['short_window'] >= data['long_window']:
            raise serializers.ValidationError("Short window must be less than long window.")
        return data

def perform_backtest(initial_investment, short_window, long_window):
    # Fetch historical data
    queryset = StockPrice.objects.filter(symbol='AAPL').order_by('date')
    if not queryset.exists():
        raise ValueError('No data available for symbol AAPL.')

    data = pd.DataFrame.from_records(queryset.values('date', 'close_price'))
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    data.sort_index(inplace=True)

    # Calculate moving averages
    data['short_mavg'] = data['close_price'].rolling(window=short_window, min_periods=1).mean()
    data['long_mavg'] = data['close_price'].rolling(window=long_window, min_periods=1).mean()

    # Generate signals
    data['signal'] = np.where(data['short_mavg'] > data['long_mavg'], 1, 0)
    data['positions'] = data['signal'].shift().fillna(0)

    # Calculate strategy returns
    data['returns'] = data['close_price'].pct_change().fillna(0)
    data['strategy_returns'] = data['returns'] * data['positions']

    # Calculate cumulative returns
    data['cumulative_returns'] = (1 + data['strategy_returns']).cumprod() * initial_investment

    # Calculate performance metrics
    total_return = (data['cumulative_returns'].iloc[-1] - initial_investment) / initial_investment * 100
    max_drawdown = ((data['cumulative_returns'].cummax() - data['cumulative_returns']) / data['cumulative_returns'].cummax()).max() * 100
    number_of_trades = data['positions'].diff().abs().sum()

    performance = {
        'total_return': total_return,
        'max_drawdown': max_drawdown,
        'number_of_trades': int(number_of_trades),
    }

    return data, performance

class BacktestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return self.run_backtest(request)

    def post(self, request):
        return self.run_backtest(request)

    def run_backtest(self, request):
        # Use serializer for validation
        if request.method == 'GET':
            serializer = BacktestSerializer(data=request.query_params)
        else:  # POST
            serializer = BacktestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        initial_investment = serializer.validated_data['initial_investment']
        short_window = serializer.validated_data['short_window']
        long_window = serializer.validated_data['long_window']

        try:
            data, performance = perform_backtest(initial_investment, short_window, long_window)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(performance, status=status.HTTP_200_OK)

class ReportView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return self.generate_report(request.query_params)

    def post(self, request):
        return self.generate_report(request.data)

    def generate_report(self ,params):
        # Use serializer for validation
        serializer = BacktestSerializer(data = params)
        if not serializer.is_valid():
            return Response(serializer.errors ,status = status.HTTP_400_BAD_REQUEST)

        initial_investment = serializer.validated_data['initial_investment']
        short_window = serializer.validated_data['short_window']
        long_window = serializer.validated_data['long_window']

        try:
            data ,performance = perform_backtest(initial_investment ,short_window ,long_window)
        except ValueError as e:
            return Response({'error': str(e)} ,status = status.HTTP_400_BAD_REQUEST)

        # Plot the equity curve
        fig ,ax = plt.subplots(figsize = (10 ,6))
        ax.plot(data.index ,data['cumulative_returns'] ,label = 'Strategy Equity Curve')
        ax.set_title('Backtest Equity Curve')
        ax.set_xlabel('Date')
        ax.set_ylabel('Portfolio Value')
        ax.legend()
        plt.tight_layout()

        # Save the plot to a BytesIO buffer
        buffer = BytesIO()
        plt.savefig(buffer ,format = 'png')
        plt.close(fig)
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        # Generate PDF report
        pdf_buffer = BytesIO()
        p = canvas.Canvas(pdf_buffer)
        p.drawString(50 ,800 ,"Backtest Performance Report")

        # Embed the chart image into the PDF
        image = ImageReader(BytesIO(image_png))
        p.drawImage(image ,50 ,400 ,width = 500 ,height = 300)

        # Add performance metrics to the PDF
        p.drawString(50 ,380 ,f"Total Return: {performance['total_return']:.2f}%")
        p.drawString(50 ,360 ,f"Max Drawdown: {performance['max_drawdown']:.2f}%")
        p.drawString(50 ,340 ,f"Number of Trades: {performance['number_of_trades']}")

        # Save and return the PDF
        p.showPage()
        p.save()

        pdf_buffer.seek(0)
        return HttpResponse(pdf_buffer ,content_type = 'application/pdf')
