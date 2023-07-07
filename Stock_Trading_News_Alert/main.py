import requests
import smtplib
import KEYS

stock_request = requests.get(KEYS.STOCK_ENDPOINT, params=KEYS.stock_params)
stock_request.raise_for_status()
stock_data = stock_request.json()["Time Series (Daily)"]
stock_data_list = [value for (key, value) in stock_data.items()]
yesterday_stock_data = stock_data_list[0]
yesterday_stock_closing_data = yesterday_stock_data["4. close"]

two_days_stock_data = stock_data_list[1]
two_days_stock_closing_data = two_days_stock_data["4. close"]

difference = abs(float(yesterday_stock_closing_data) - float(two_days_stock_closing_data))
diff_sign = "🔺"
if (float(yesterday_stock_closing_data) - float(two_days_stock_closing_data)) <= 0:
    diff_sign = "🔻"

diff_percent = (difference / float(two_days_stock_closing_data)) * 100

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
news_request = requests.get(NEWS_ENDPOINT, params=KEYS.news_params)
news_request.raise_for_status()
five_articles = news_request.json()["articles"][:5]
five_articles_list = [f"HeadLine: {article['title']} \nBrief: {article['description']}" for article in five_articles]

if diff_percent > KEYS.DIFF_PERCENTAGE:
    for article in five_articles_list:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()  # safe connection
            connection.login(user=KEYS.sender, password=KEYS.password)
            connection.sendmail(
                from_addr=KEYS.sender,
                to_addrs=KEYS.receivers,
                msg=f"{diff_sign}{diff_percent}\n{article}"
            )
