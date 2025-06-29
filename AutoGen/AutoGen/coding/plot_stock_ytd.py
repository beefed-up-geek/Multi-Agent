# filename: plot_stock_ytd.py
import pandas as pd
import matplotlib.pyplot as plt

# Prices retrieved from previous execution
meta_current = 733.6300048828125
meta_start_of_year = 502.4994201660156
tesla_current = 323.6300048828125
tesla_start_of_year = 197.8800048828125

# Prepare data for CSV and plotting
data = {
    'Stock': ['META', 'TESLA'],
    'Price at Beginning of Year': [meta_start_of_year, tesla_start_of_year],
    'Current Price': [meta_current, tesla_current],
    'YTD Gain (%)': [46.00, 63.55]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('stock_price_ytd.csv', index=False)

# Plotting
plt.figure(figsize=(10, 6))
plt.bar(df['Stock'], df['YTD Gain (%)'], color=['blue', 'orange'])
plt.title('Year-to-Date Gain for META and TESLA')
plt.xlabel('Stock')
plt.ylabel('YTD Gain (%)')
plt.ylim(0, 100)
plt.grid(axis='y')

# Save the plot
plt.savefig('stock_price_ytd.png')
plt.close()