# filename: fetch_stock_prices.py
import yfinance as yf
from datetime import datetime

# Define the stock symbols
meta_symbol = 'META'
tesla_symbol = 'TSLA'

# Get today's date
today = datetime.now().date()

# Function to fetch stock prices
def fetch_stock_data(symbol):
    try:
        current_price = yf.Ticker(symbol).history(period='1d')['Close'].iloc[-1]
        start_of_year_price = yf.Ticker(symbol).history(start='2025-01-01', end='2025-01-02')['Close'].iloc[0]
        return current_price, start_of_year_price
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None, None

# Fetch prices for META and TESLA
meta_current, meta_start_of_year = fetch_stock_data(meta_symbol)
tesla_current, tesla_start_of_year = fetch_stock_data(tesla_symbol)

# Print the results
if meta_current is not None and meta_start_of_year is not None:
    print(f"Current price of META: {meta_current}")
    print(f"Price of META at the beginning of the year: {meta_start_of_year}")
else:
    print("Could not retrieve META stock data.")

if tesla_current is not None and tesla_start_of_year is not None:
    print(f"Current price of TESLA: {tesla_current}")
    print(f"Price of TESLA at the beginning of the year: {tesla_start_of_year}")
else:
    print("Could not retrieve TESLA stock data.")