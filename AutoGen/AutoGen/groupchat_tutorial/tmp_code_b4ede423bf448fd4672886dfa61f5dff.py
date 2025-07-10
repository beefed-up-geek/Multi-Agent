import numpy as np

# Hypothetical inputs
current_price = 250  # Current price of TSLA
expected_growth_rate_conservative = 0.05  # 5% growth
expected_growth_rate_base = 0.10  # 10% growth
expected_growth_rate_aggressive = 0.15  # 15% growth
years = [1, 3]  # 1 year and 3 years

def simulate_expected_return(current_price, growth_rate, years):
    return current_price * (1 + growth_rate) ** years

# Calculate expected returns
expected_returns = {
    '1 Year': {
        'Conservative': simulate_expected_return(current_price, expected_growth_rate_conservative, 1),
        'Base': simulate_expected_return(current_price, expected_growth_rate_base, 1),
        'Aggressive': simulate_expected_return(current_price, expected_growth_rate_aggressive, 1),
    },
    '3 Years': {
        'Conservative': simulate_expected_return(current_price, expected_growth_rate_conservative, 3),
        'Base': simulate_expected_return(current_price, expected_growth_rate_base, 3),
        'Aggressive': simulate_expected_return(current_price, expected_growth_rate_aggressive, 3),
    }
}

expected_returns