import yfinance as yf

# Get the data for the stock Apple by specifying the stock ticker, start date, and end date
meta_data = yf.download('META', start='2022-01-01', end=current_date)
tesla_data = yf.download('TSLA', start='2022-01-01', end=current_date)

# Calculate the YTD gain for META and TESLA
meta_ytd_gain = ((meta_data['Close'][-1] - meta_data['Close'][0]) / meta_data['Close'][0]) * 100
tesla_ytd_gain = ((tesla_data['Close'][-1] - tesla_data['Close'][0]) / tesla_data['Close'][0]) * 100

print("META YTD gain:", meta_ytd_gain)
print("TESLA YTD gain:", tesla_ytd_gain)