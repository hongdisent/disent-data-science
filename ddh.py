import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Constants
S0 = 100  # Initial stock price
K = 100   # Strike price of the option
T = 1     # Time to maturity (1 year)
r = 0.05  # Risk-free rate
sigma = 0.2  # Volatility
dt = 1/252  # Time step (daily)
N = 252  # Number of trading days (1 year)
option_type = 'call'  # Type of the option (call or put)

# Black-Scholes Model for European Option Pricing
def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        option_price = S * norm_cdf(d1) - K * np.exp(-r * T) * norm_cdf(d2)
        delta = norm_cdf(d1)
    elif option_type == 'put':
        option_price = K * np.exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)
        delta = -norm_cdf(-d1)
    
    return option_price, delta

# CDF of the standard normal distribution (for Black-Scholes)
def norm_cdf(x):
    return norm.cdf(x)

# Dynamic Delta Hedging Simulation
def dynamic_delta_hedging(S0, K, T, r, sigma, dt, N, option_type='call'):
    stock_prices = [S0]  # Stock price over time
    option_prices = []  # Option price over time
    deltas = []  # Delta of the option at each step
    portfolio_values = []  # Portfolio value (stock + option hedge)
    hedge_positions = []  # Hedge position (number of shares)

    # Initial conditions
    S = S0
    portfolio_value = 0  # Initial portfolio value
    hedge_position = 0  # Initial hedge (no position in stock)
    
    # Loop over time steps
    for t in range(1, N + 1):
        # Time to maturity remaining
        time_remaining = (T - t * dt)
        
        # Get the option price and delta using the Black-Scholes model
        option_price, delta = black_scholes(S, K, time_remaining, r, sigma, option_type)
        
        # Calculate the portfolio value (stock position + option value)
        portfolio_value = hedge_position * S + option_price
        
        # Record values for plotting
        stock_prices.append(S)
        option_prices.append(option_price)
        deltas.append(delta)
        portfolio_values.append(portfolio_value)
        hedge_positions.append(hedge_position)
        
        # Rebalance the hedge to match the new delta (buy or sell the underlying stock)
        hedge_position = delta  # Adjust the hedge to the option's delta
        
        # Simulate the stock price movement (simplified random walk model)
        S = S * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * np.random.normal())

    return stock_prices, option_prices, deltas, portfolio_values, hedge_positions

# Run the simulation
stock_prices, option_prices, deltas, portfolio_values, hedge_positions = dynamic_delta_hedging(S0, K, T, r, sigma, dt, N, option_type)

# Plot the results
plt.figure(figsize=(14, 8))

plt.subplot(2, 2, 1)
plt.plot(stock_prices, label='Stock Price')
plt.title("Stock Price Over Time")
plt.xlabel("Time (Days)")
plt.ylabel("Price")
plt.legend()

plt.subplot(2, 2, 2)
plt.plot(option_prices, label='Option Price')
plt.title("Option Price Over Time")
plt.xlabel("Time (Days)")
plt.ylabel("Option Price")
plt.legend()

plt.subplot(2, 2, 3)
plt.plot(deltas, label='Delta of the Option')
plt.title("Delta of the Option Over Time")
plt.xlabel("Time (Days)")
plt.ylabel("Delta")
plt.legend()

plt.subplot(2, 2, 4)
plt.plot(portfolio_values, label='Portfolio Value')
plt.title("Portfolio Value (Hedge + Option) Over Time")
plt.xlabel("Time (Days)")
plt.ylabel("Portfolio Value")
plt.legend()

plt.tight_layout()
plt.show()
