import requests
from twilio.rest import Client

# using TSLA for this example, feel free to change it
STOCK = "TSLA"
# make sure also change COMPANY_NAME to match with STOCK
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = 'https://www.alphavantage.co/query'
# please create your own STOCK_API_KEY by visiting the alphavantage website above
STOCK_API_KEY = ''
# please create your own NEWS_API_KEY by visiting the newsapi website blow
NEWS_API_KEY = ''
NEWS_ENDPOINT = 'https://newsapi.org/v2/everything'

# please create your own twilio account to get your unique TWILIO_SID and TWILIO_AUTH_TOKEN
TWILIO_SID = ''
TWILIO_AUTH_TOKEN = ''


def send_text():
    """Sends three texts containing news about a stock to a phone number using the twilio API.
    """
    news_params = {
        'apikey': NEWS_API_KEY,
        'qInTitle': COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    print(news_response.json())
    articles = news_response.json()['articles']
    three_articles = articles[:3]

    formatted_articles = [
        f"{STOCK}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages \
            .create(
                body=article,
                # enter from number (you get this from your twilio account: +1xxxxxxxxxx)
                from_='+1',
                # receiving number (+1xxxxxxxxxx)
                to='+1'
            )


stock_params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': STOCK_API_KEY,
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data['4. close']
day_before_yesterday = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday['4. close']
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = '🔺'
else:
    up_down = '🔻'

diff_percent = round((difference / float(yesterday_closing_price)) * 100)

# can change the STOCK's different percentage and comparison sign here
if diff_percent > 5:
    send_text()
