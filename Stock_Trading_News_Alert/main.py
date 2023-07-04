import requests
import smtplib

sender = "sender@gmail.com"
password = "password"
receivers = "receivers@gmail.com"

STOCK_API_KEY = "STOCK_API_KEY"
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
DIFF_PERCENTAGE = 4

NEWS_API_KEY = "NEWS_API_KEY"

stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
stock_request = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_request.raise_for_status()
stock_data = stock_request.json()["Time Series (Daily)"]
stock_data_list = [value for (key, value) in stock_data.items()]
yesterday_stock_data = stock_data_list[0]
yesterday_stock_closing_data = yesterday_stock_data["4. close"]

two_days_stock_data = stock_data_list[1]
two_days_stock_closing_data = two_days_stock_data["4. close"]

difference = abs(float(yesterday_stock_closing_data) - float(two_days_stock_closing_data))
if (float(yesterday_stock_closing_data) - float(two_days_stock_closing_data)) < 0:
    diff_sign = "-"
elif float(yesterday_stock_closing_data) - float(two_days_stock_closing_data) > 0:
    diff_sign = "+"
else:
    diff_sign = ""
diff_percent = (difference / float(two_days_stock_closing_data)) * 100

news_params = {
    "apiKey": NEWS_API_KEY,
    "q": COMPANY_NAME,
    "sortBy": "popularity"
}

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
news_request = requests.get(NEWS_ENDPOINT, params=news_params)
news_request.raise_for_status()
five_articles = news_request.json()["articles"][:5]
five_articles_list = [f"HeadLine: {article['title']} \nBrief: {article['description']}" for article in five_articles]

if diff_percent > DIFF_PERCENTAGE:
    for article in five_articles_list:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()  # safe connection
            connection.login(user=sender, password=password)
            connection.sendmail(
                from_addr=sender,
                to_addrs=receivers,
                msg=f"{diff_sign}{diff_percent}\n{article}"
            )
