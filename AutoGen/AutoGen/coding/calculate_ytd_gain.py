# filename: calculate_ytd_gain.py
# Prices retrieved from previous execution
meta_current = 733.6300048828125
meta_start_of_year = 502.4994201660156
tesla_current = 323.6300048828125
tesla_start_of_year = 197.8800048828125

# Function to calculate year-to-date gain
def calculate_ytd_gain(current_price, start_of_year_price):
    return ((current_price - start_of_year_price) / start_of_year_price) * 100

# Calculate YTD gains
meta_ytd_gain = calculate_ytd_gain(meta_current, meta_start_of_year)
tesla_ytd_gain = calculate_ytd_gain(tesla_current, tesla_start_of_year)

# Print the results
print(f"Year-to-Date Gain for META: {meta_ytd_gain:.2f}%")
print(f"Year-to-Date Gain for TESLA: {tesla_ytd_gain:.2f}%")