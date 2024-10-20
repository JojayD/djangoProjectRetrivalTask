import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
# url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=IBM&apikey=demo'
# r = requests.get(url)
# data = r.json()
# dict_data = dict(data)
# print(dict_data)
# for key, value in data.items():
# 	for element1, element2 in value.items():
# 		print(element1, element2)
# print(data)
dict_data={
    'Meta Data': {
        '1. Information': 'Monthly Adjusted Prices and Volumes',
        '2. Symbol': 'IBM',
        '3. Last Refreshed': '2024-10-18',
        '4. Time Zone': 'US/Eastern'
    },
    'Monthly Adjusted Time Series': {
        '2024-10-18': {
            '1. open': '220.6300',
            '2. high': '237.3700',
            '3. low': '215.7980',
            '4. close': '232.2000',
            '5. adjusted close': '232.2000',
            '6. volume': '51109973',
            '7. dividend amount': '0.0000'
        },
        '2024-09-30': {
            '1. open': '201.9100',
            '2. high': '224.1500',
            '3. low': '199.3350',
            '4. close': '221.0800',
            '5. adjusted close': '221.0800',
            '6. volume': '83415811',
            '7. dividend amount': '0.0000'
        },
        '2024-08-30': {
            '1. open': '192.8100',
            '2. high': '202.1700',
            '3. low': '181.8100',
            '4. close': '202.1300',
            '5. adjusted close': '202.1300',
            '6. volume': '65453729',
            '7. dividend amount': '1.6700'
        }
    }
}

