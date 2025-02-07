import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import minimize
from dateroll import ddh

def get_stock_returns(tickers, start, end):
    """Fetch historical adjusted close prices and compute daily returns."""
    data = yf.download(tickers, start=start, end=end)['Close']
    if data.isnull().values.any():
        raise ValueError("One or more tickers are invalid or have missing data.")
    returns = data.pct_change().dropna()
    return returns

def optimize_portfolio(returns, objective_function):
    """Optimize portfolio using user-defined objective function."""
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    num_assets = len(mean_returns)
    initial_weights = np.ones(num_assets) / num_assets  # Equal allocation
    bounds = [(0, 1) for _ in range(num_assets)]  # No short-selling
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})  # Sum of weights = 1
    
    result = minimize(
        objective_function, initial_weights,
        args=(mean_returns, cov_matrix),
        method='SLSQP', bounds=bounds, constraints=constraints
    )
    
    
    return result.x  # Optimal weights

# Example usage
def sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate=0.0):
    """Calculate the negative Sharpe ratio (for minimization)."""
    portfolio_return = np.dot(weights, mean_returns)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    sharpe = (portfolio_return - risk_free_rate) / portfolio_volatility
    return -sharpe  # Negative for minimization

def min_volatility(weights, mean_returns, cov_matrix):
    """Minimize portfolio volatility."""
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return portfolio_volatility

def max_return(weights, mean_returns, cov_matrix):
    """Maximize portfolio return (by minimizing negative return)."""
    return -np.dot(weights, mean_returns)

def printTickerAndWeight(tickers, optimal_weights,objective_function):
    print("Optimal Portfolio Weights with objective function {}:".format(objective_function.__name__))
    for ticker, weight in zip(tickers, optimal_weights):
        print(f"{ticker}: {weight:.4f}")


tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
start_date = ddh('t-2y')

end_date = ddh("t")
objective_function = min_volatility


returns = get_stock_returns(tickers, start_date, end_date)

optimal_weights = optimize_portfolio(returns, objective_function)

printTickerAndWeight(tickers, optimal_weights,objective_function)

