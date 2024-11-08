import pandas as pd
import numpy as np

# Function to calculate CAGR
def calculate_cagr(df, start_date, end_date):
    total_days = (end_date - start_date).days
    total_years = total_days / 365.25
    cagr = (df['Port_Value'].iloc[-1] / df['Port_Value'].iloc[0]) ** (1 / total_years) - 1
    return cagr

# Function to calculate Sharpe Ratio
def calculate_sharpe_ratio(df, risk_free_rate=0.01):
    excess_return = df['Return'] - risk_free_rate / 252
    sharpe_ratio = np.mean(excess_return) / np.std(excess_return) * np.sqrt(252)
    return sharpe_ratio

# Function to calculate Maximum Drawdown
def calculate_max_drawdown(df):
    cumulative_return = (1 + df['Return']).cumprod()
    peak = cumulative_return.cummax()
    drawdown = (cumulative_return - peak) / peak
    max_drawdown = drawdown.min()
    return max_drawdown
	
#  Inputs:
#   w - weights per asset in each column, there is a column of 'Date' in Datetime
#   full_returns:  return rates per asset in each column, the index is DatetimeIndex and named as 'Date'
#
def simple_backtest(w, full_return, rm, obj, r_int):
    
    mdf = pd.merge(full_return.reset_index()[['Date']], w, on='Date', how='left').ffill().round(5)
    # display(mdf)
    weights = mdf.drop(columns=['Date']).to_numpy()
    print("weights array size: ", weights.shape)
    # display(weights[-10:-1])

    Portfolio = full_return.reset_index().copy()
    # display(Portfolio)
    assets_names = Portfolio.drop(columns=['Date']).columns.to_list()
    # display(assets_names)
    
    # Calculate portfolio daily returns
    Portfolio['Return'] = (weights * Portfolio[assets_names]).sum(axis=1)
    
    # Calculate portfolio value assuming initial investment of $100,000
    initial_investment = 100000
    Portfolio['Port_Value'] = initial_investment * (1 + Portfolio['Return']).cumprod()
    
    # display(Portfolio)
    
    # Calculate CAGR
    start_date = Portfolio['Date'].iloc[0]
    end_date = Portfolio['Date'].iloc[-1]
    cagr = calculate_cagr(Portfolio, start_date, end_date)
    
    # Calculate Sharpe Ratio
    sharpe_ratio = calculate_sharpe_ratio(Portfolio)
    
    # Calculate Maximum Drawdown
    max_drawdown = calculate_max_drawdown(Portfolio)
    
    print(f"CAGR: {cagr:.2%}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"Maximum Drawdown: {max_drawdown:.2%}")
    return {'Risk_measure':rm, 'Objective':obj, 
            'R_Interval': r_int, 'Max DrawDown':max_drawdown, 
            'CAGR': cagr, 'Sharpe Ratio':sharpe_ratio},  Portfolio[['Date','Return']]
    
