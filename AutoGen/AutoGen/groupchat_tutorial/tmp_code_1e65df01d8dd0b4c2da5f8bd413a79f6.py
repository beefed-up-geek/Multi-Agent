import numpy as np
import pandas as pd

# Sample historical closing prices for TSLA (replace with actual data)
closing_prices = [700, 720, 750, 780, 800, 820, 850, 870, 900, 950]  # Example data
returns = np.diff(closing_prices) / closing_prices[:-1]

# Define scenarios
scenarios = {
    'Conservative': 0.05,  # 5% expected return
    'Base': 0.10,          # 10% expected return
    'Aggressive': 0.15     # 15% expected return
}

# Simulate expected returns for 1 year and 3 years
def simulate_returns(initial_investment, years, scenario):
    return initial_investment * (1 + scenario) ** years

initial_investment = 10000  # Example investment amount
results = {}

for label, rate in scenarios.items():
    results[label] = {
        '1 Year': simulate_returns(initial_investment, 1, rate),
        '3 Years': simulate_returns(initial_investment, 3, rate)
    }

# Print the results in a simple format
print("Expected Returns Simulation:")
for scenario, values in results.items():
    print(f"{scenario}: 1 Year = {values['1 Year']:.2f}, 3 Years = {values['3 Years']:.2f}")