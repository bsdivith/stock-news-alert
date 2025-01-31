import requests
from datetime import date
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
TWILIO_ENDPOINT = ""

STOCK_API = "<your alpha vantage api>"
NEWS_API = "<your news api>"
TWILIO_API = ""

TWILIO_ACCOUNT_SID = "<your sid>"
TWILIO_AUTHENTICATION_TOKEN = "<your twilio auth token>"

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_params = {
    "function" :"TIME_SERIES_DAILY",
    "apikey" : STOCK_API,
    "symbol" : STOCK_NAME,
}

response = requests.get(STOCK_ENDPOINT, stock_params)
data = response.json()['Time Series (Daily)']
data_list = [value for (key,value) in data.items()]

yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data['4. close']

day_before_yesterday = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday['4. close']


gap = (float(yesterday_closing_price) - float(day_before_yesterday_closing_price))

percent_change = (gap/float(yesterday_closing_price))*100
if percent_change>0:
    emoji = "🔺"
else:
    emoji="🔻"
print(data)

today = date.today()
day = today.day
yesterday = day-1
day_before_yesterday = yesterday-1

print(today, yesterday_closing_price,day_before_yesterday_closing_price,gap, percent_change)


if abs(percent_change)>2:
    print("Yes")
    news_params = {
        "qInTitle": COMPANY_NAME,
        "apikey": NEWS_API,
        "sortBy": "popularity",

    }
    news_response = requests.get(NEWS_ENDPOINT, news_params)
    articles = news_response.json()['articles']
    three_articles = articles[0:3]
    # print(three_articles)

    formatted_articles = [f"TSLA: {emoji}{round(percent_change)}% /n Headline:{article["title"]}.\n Brief:{article['description']}." for article in three_articles]
    print(formatted_articles)

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTHENTICATION_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(body=article,from_="<your twilio virtual number>",to="<your number>" )




    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number.






#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

