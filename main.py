import datetime

import requests
from twilio.rest import Client

from config import config

# Datetime variables
TODAY = datetime.date.today()
YESTERDAY = str(TODAY - datetime.timedelta(days=1))
TWO_DAYS_AGO = str(TODAY - datetime.timedelta(days=2))

# Twilio authentication
ACCOUNT_SID = config["ACCOUNT_SID"]
AUTH_TOKEN = config["AUTH_TOKEN"]

# Stocks API variables
STOCK = "MSFT"
STOCKS_API_KEY = config["STOCKS_API_KEY"]
STOCK_URL = "https://www.alphavantage.co/query?"

# News API variables
NEWS_URL = "https://newsapi.org/v2/everything?"
NEWS_API_KEY = config["NEWS_API_KEY"]
COMPANY_NAME = "Microsoft"

# Params for alphavantage api
stock_parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": STOCKS_API_KEY,
}

# params for newsapi
news_parameters = {
    "q": COMPANY_NAME,
    "from": str(TODAY),
    "sortBy": "popularity",
    "apiKey": NEWS_API_KEY,
}

# connect to stocks api and grab data
connection = requests.get(STOCK_URL, params=stock_parameters)
connection.raise_for_status()
data = connection.json()["Time Series (Daily)"]

# grab close data and get percent diff
stock_yesterday = float(data[YESTERDAY]["4. close"])
stock_two_days_ago = float(data[TWO_DAYS_AGO]["4. close"])
percent_diff = round((stock_yesterday - stock_two_days_ago) / stock_two_days_ago * 100)

# if there is a bigger than 2% change in close data, grab current headline news
if percent_diff >= 2 or percent_diff <= -2:
    # Get data from news api
    connection = requests.get(NEWS_URL, params=news_parameters)
    connection.raise_for_status()
    data = connection.json()
    articles = data["articles"]

    # loop through only the first 3 articles
    text_content = ""
    for i in range(3):
        title = articles[i]["title"]
        description = articles[i]["description"]

        text_content += f"Headline: {title}\n"
        text_content += f"Brief: {description}\n"

    # for the positive / negative sign
    if percent_diff > 0:
        percent_sign = "🔺"
    else:
        percent_sign = "🔻"

    # send twilio sms
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        body=f"{STOCK}: {percent_sign}{percent_diff}%\n{text_content}",
        from_=config["TWILIO_NUMBER"],
        to=config["MY_NUMBER"],
    )

    print(message.status)
else:
    print(f"No big stock price changes in {COMPANY_NAME}")
