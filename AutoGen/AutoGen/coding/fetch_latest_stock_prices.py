# filename: fetch_latest_stock_prices.py
import yfinance as yf

# Define the stock symbols
meta_symbol = 'META'
tesla_symbol = 'TSLA'

# Function to fetch stock prices
def fetch_latest_stock_data(symbol):
    try:
        # Fetch current price
        current_price = yf.Ticker(symbol).history(period='1d')['Close'].iloc[-1]
        
        # Fetch the last available price
        historical_data = yf.Ticker(symbol).history(period='1y')
        start_of_year_price = historical_data['Close'].iloc[0] if not historical_data.empty else None
        
        return current_price, start_of_year_price
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None, None

# Fetch prices for META and TESLA
meta_current, meta_start_of_year = fetch_latest_stock_data(meta_symbol)
tesla_current, tesla_start_of_year = fetch_latest_stock_data(tesla_symbol)

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