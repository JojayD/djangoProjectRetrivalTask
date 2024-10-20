import os
import django
from datetime import date
from stock_data.data import dict_data

from django.core.management.base import BaseCommand
from decouple import config
from datetime import datetime, timedelta
import requests
os.environ.setdefault('DJANGO_SETTINGS_MODULE' ,
                      'djangoProjectRetrivalTask.settings')  # replace djangoProjectRetrivalTask with your project name
django.setup()

from stock_data.models import StockPrice



class Command(BaseCommand):
	help = "Commnad to get stock price data"
	SECRET_KEY = config('SECRET_KEY')
	DATABASE_PW = config('DATABASE_PW')
	VANTAGE_API_KEY = config('VANTAGE_API_KEY')

	def is_ISO8601(self,date_string):
		try:
			datetime.fromisoformat(date_string)
			print("True")
			return True
		except ValueError:
			return False

	def handle(self ,*args ,**options):

		VANTAGE_API_KEY = config('VANTAGE_API_KEY')
		SYMBOL = 'AAPL'
		BASE_URL = 'https://www.alphavantage.co/query'
		params = {
			'function': 'TIME_SERIES_MONTHLY_ADJUSTED' ,
			'symbol': SYMBOL ,
			'apikey': VANTAGE_API_KEY
		}


		records_created = 0
		try:
			# response = requests.get(BASE_URL ,params = params)
			# # data = response.json()

			# print(dict_data)
			# response.raise_for_status()
			# time_series = data.get('Monthly Adjusted Time Series' ,{})  # Updated for monthly data

			monthly_adjusted_data = dict_data['Monthly Adjusted Time Series']
			print(monthly_adjusted_data)
			records_created = 0
			two_years_ago = datetime.now().date() - timedelta(days = 730)

			for date_str ,monthly_data in monthly_adjusted_data.items():
				print(date_str, monthly_data)
				date = datetime.strptime(date_str ,'%Y-%m-%d').date()
				if date < two_years_ago:
					continue

				obj ,created = StockPrice.objects.update_or_create(
					symbol = SYMBOL ,
					date = date ,
					defaults = {
						'open_price': float(monthly_data['1. open']) ,
						'high_price': float(monthly_data['2. high']) ,
						'low_price': float(monthly_data['3. low']) ,
						'close_price': float(monthly_data['4. close']) ,
						'volume': int(monthly_data['6. volume']) ,
					}
				)
				if created:
					records_created += 1


			self.stdout.write(self.style.SUCCESS(f'Successfully fetched data. Records created: {records_created}'))

		except requests.exceptions.HTTPError as errh:
			self.stderr.write(f'HTTP Error: {errh}')
		except requests.exceptions.ConnectionError as errc:
			self.stderr.write(f'Error Connecting: {errc}')
		except requests.exceptions.Timeout as errt:
			self.stderr.write(f'Timeout Error: {errt}')
		except requests.exceptions.RequestException as err:
			self.stderr.write(f'Oops: Something Else {err}')
		except Exception as e:
			self.stderr.write(f'An error occurred: {e}')


