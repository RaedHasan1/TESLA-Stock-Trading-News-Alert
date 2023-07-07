STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

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

news_params = {
    "apiKey": NEWS_API_KEY,
    "q": COMPANY_NAME,
    "sortBy": "popularity"
}