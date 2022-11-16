# Stock News SMS Reporter

Uses three API's: 
- Stock Price API: https://www.alphavantage.co/
- Stock News API: https://newsapi.org/
- SMS API: https://www.twilio.com/

Grabs the stock information for the specified stock from alphavantage API and 
calculates the percent difference between its closing price from two days ago and
yesterday. If the percent different is more than an "x" amount (in my case, 2%), 
then grab the top 3 headline news for the stock, and send me an SMS of it's title
and brief descriptions.
