import numpy as np
import random
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import alpaca_trade_api as tradeapi
from dotenv import load_dotenv
import os
from alpaca_trade_api.rest import REST, TimeFrame
import hvplot.pandas
from scipy.interpolate import interp1d
import datetime as dt







def fetch_stock_data(start_date, end_date, stock_list):
    # Grabbing all necessary alpaca information
    alpaca_api_key = os.getenv("ALPACA_API_KEY")
    alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")
    api = REST(alpaca_api_key, alpaca_secret_key, base_url = 'https://paper-api.alpaca.markets')
    start_date_iso = pd.Timestamp(start_date, tz = 'America/New_York').isoformat()
    end_date_iso = pd.Timestamp(end_date, tz = 'America/New_York').isoformat()
    # Creating dataframe
    df_stock = api.get_bars(stock_list, TimeFrame.Day, start = start_date_iso, end = end_date_iso).df
    # Selecting only close price data for each stock, and concatenating them into one dataframe
    dfs = {}
    for stock in stock_list:
        stock_df = df_stock.loc[df_stock.symbol == stock]['close']
        dfs[stock] = stock_df
    concatenated_df = pd.concat(dfs.values(), axis = 1, keys = stock_list)
    # Resetting index to have only date information
    concatenated_df.reset_index(inplace = True)
    concatenated_df.timestamp = pd.to_datetime(concatenated_df.timestamp.dt.date)
    concatenated_df.set_index('timestamp', inplace = True)
    return concatenated_df

def weights(stock_list, repeats):
    full_list = []
    for _ in range(repeats):
        lst = []
        while sum(lst) != 1:
            lst = np.random.randint(1,100, len(stock_list))
            lst = [round(x / sum(lst),4) for x in lst]
        full_list.append(lst)
    # If only has one set of weights, return a single list, not list of lists inside
    if repeats == 1:
        full_list = full_list[0]
    return full_list

def annual_portfolio_return(df, weight_list):
    # Calculate the daily returns of stocks
    daily_return = df.pct_change().dropna()
    # Calculate the mean of daily returns, and dot product it with their weights to find the portfolio mean. Multiply the result by 252 to get the annual mean return
    portfolio_mean = daily_return.dot(weight_list).mean() * 252
    return portfolio_mean

def annual_portfolio_risk(df, weight_list):
    # Calculate the daily retuns of stocks
    daily_return = df.pct_change()
    # Find covariance matrix of the stocks
    cov_matrix = daily_return.cov()
    # Change weight lists into a vector
    weight_mat = np.matrix(weight_list)
    # Use the formula for portfolio risk (standard deviation) which is (w * sigma * w.T)^(0.5) where w is the weight vector and sigma is the covariance matrix. Multiply the result by np.sqrt(252) to get the annual risk
    portfolio_risk = np.sqrt(np.dot(np.dot(weight_mat, cov_matrix), weight_mat.T)).item() * np.sqrt(252)
    return portfolio_risk

def yearly_portfolio_info(df, weight_list):
    # Only extract Year data from the index
    new_df = df.reset_index()
    new_df.timestamp = new_df.timestamp.dt.year
    new_df.set_index('timestamp', inplace = True)
    # Loop through the dataframe year by year, calculate portfolio returns and risks, then store those info into a list. Column list contains the year information
    yearly_returns = []
    yearly_risks = []
    column_list = []
    for i in range(new_df.index.nunique()):
        yearly_df = new_df.loc[new_df.index == new_df.index.unique()[i]]
        yearly_returns.append(annual_portfolio_return(yearly_df, weight_list))
        yearly_risks.append(annual_portfolio_risk(yearly_df, weight_list))
        column_list.append(new_df.index.unique()[i])
    # Put all the informations into a single dataframe
    final_df = pd.DataFrame([yearly_returns, yearly_risks], index = ['Return', 'Risk'], columns = column_list)
    # Change the orientation and multiply by 100 to show values in percentage
    final_df = final_df.T * 100
    plot = final_df.hvplot.bar(frame_width = 700, frame_height = 450, ylabel = 'Values (%)', xlabel = 'Year', title = 'Yearly portfolio risks and returns')
    display(plot)

def opportunity_set(df, my_weights, repeats, risk_free_return = 0, cal = False):
    # Create nsims number of weight sets using weights function
    weight_list = weights(df.columns.tolist(), repeats)
    return_list = []
    std_dev_list = []
    # For each weight set, calculate annual portfolio returns and risks, then append them to return_list and std_dev_list. Then put them together into one dataframe
    for i in weight_list:
        return_list.append(annual_portfolio_return(df, i))
        std_dev_list.append(annual_portfolio_risk(df, i))
    new_df = pd.DataFrame([return_list, std_dev_list], index = ['portfolio_return', 'portfolio_risk'])
    # Change the dataframe's orientation and multiply by 100 to show values in percentages
    new_df = new_df.T * 100
    # Calculate sharpe ratio
    new_df['sharpe_ratio'] = (new_df.portfolio_return - risk_free_return)/ new_df.portfolio_risk
    
    # Find indexes of the safest portfolio and optimal risky portfolio
    safest_portfolio_index = new_df[new_df.portfolio_risk == new_df.portfolio_risk.min()].index[0]
    safest_portfolio_weights = weight_list[safest_portfolio_index]
    optimal_risky_portfolio_index = new_df[new_df.sharpe_ratio == new_df.sharpe_ratio.max()].index[0]
    optimal_risky_portfolio_weights = weight_list[optimal_risky_portfolio_index]
    # Print weight composition of your portfolio, optimal risky portfolio, and safest portfolio
    print(f'Your portfolio consists of: '),
    for i in range(df.shape[1]):
        print(f'{(my_weights[i] * 100):.2f}% of {df.columns[i]}'),
    print('-'*30)
    print(f'Optimal risky portfolio consists of: '),
    for i in range(df.shape[1]):
        print(f'{(optimal_risky_portfolio_weights[i] * 100):.2f}% of {df.columns[i]}'),
    print('-'*30) 
    print(f'Safest portfolio consists of: '),
    for i in range(df.shape[1]):
        print(f'{(safest_portfolio_weights[i] * 100):.2f}% of {df.columns[i]}'),
    print('-'*30)
    # Plot all the points on a scatter plot
    plt.figure(figsize = (10,7))
    plt.scatter(x = new_df.portfolio_risk, y = new_df.portfolio_return, s = 0.3, alpha = 0.5)
    plt.scatter(x = annual_portfolio_risk(df, safest_portfolio_weights) * 100, y = annual_portfolio_return(df, safest_portfolio_weights) * 100, color = 'mediumseagreen', label = 'Safest portfolio point')
    plt.scatter(x = annual_portfolio_risk(df, optimal_risky_portfolio_weights) * 100, y = annual_portfolio_return(df, optimal_risky_portfolio_weights) * 100, color = 'gold', label = 'Optimal risky portfolio point')
    plt.scatter(x = annual_portfolio_risk(df, my_weights) * 100, y = annual_portfolio_return(df, my_weights) * 100, color = 'k', label = 'Your portfolio', marker = '*')
    plt.xlabel('Risk (%)')
    plt.ylabel('Return (%)')
    plt.title('Return (%) vs. Risk (%)')
    plt.legend()
    # If cal is True, return a capital allocation line using the risk free rate.
    if cal == True:
        a = new_df[new_df.sharpe_ratio == new_df.sharpe_ratio.max()].sharpe_ratio.item()
        x = np.arange(0,25)
        y = risk_free_return + a * x
        plt.plot(x,y)
        plt.xlim(0,30)
        plt.ylim(0,30)
       
    return optimal_risky_portfolio_weights
    
def mc_sim(df, weight_list, timeframe, nsims, investment_amount = 1, kind = 'line'):
    # Calulate the daily portfolio return and risk
    port_return = annual_portfolio_return(df, weight_list) / 252
    port_risk = annual_portfolio_risk(df, weight_list) / np.sqrt(252)
    # Create a framework for all the simulations
    all_simulations = np.full(shape = (timeframe, nsims), fill_value = 0.0)
    # For each simulation, it generates one numpy array, assigns randomless according to the portfolio return and risk, then finds cumulative return of that simulation.
    # Each created simulation then will be interted into the all_simulations framework
    for i in range(0, nsims):
        one_simulation = np.ones(shape = (timeframe, 1))
        rand = np.random.normal(port_return, port_risk, timeframe).T.reshape((timeframe,1))
        simulations = np.cumprod(one_simulation + rand) * investment_amount
        all_simulations[:,i] = simulations
    # Convert the created simulations into dataframe
    sim_df = pd.DataFrame(all_simulations)
    # If line is chosen, line graphs of all the simulations will be displayed
    if kind == 'line':
        plt.plot(all_simulations)
        plt.title('Monte Carlo Simulation of portfolio')
        plt.xlabel('Days')
        plt.ylabel('Portfolio value')
    # If kde is chosen, the KDE plot of the simulations' last day will be displated
    elif kind == 'kde':
        ax = sim_df.iloc[-1,:].hvplot.kde(alpha = 0.1, title = 'KDE plot of the end result of Monte Carlo Simulation', yformatter = '%.5f', frame_width = 700, frame_height = 400)
        display(ax)
    # If range is chosen, graph that has confidence intervals and interpolated median line is drawn
    elif kind == 'visualize_ci':
        sim_df_copy = sim_df.copy()
        # 2.5 and 97.5 will form 95% CI, and 25 and 75 will form 50% CI range
        percentiles = [2.5, 25, 75, 97.5]
        # Find median for each day's simulation results
        sim_df_copy['median'] = sim_df_copy.median(axis = 1)
        # Find percentiles for each day's simulation results using the above percentile list
        for i in range(len(percentiles)):
            sim_df_copy[f'percentile_{i}'] = sim_df_copy.iloc[:,:-(i+1)].apply(lambda row: np.percentile(row, percentiles[i]), axis = 1)
        
        # Since actual median and percentile values will draw rough lines, scipy.interpolate interp1d was used to smooth those lines for better presentation
        x = np.linspace(0, sim_df_copy.shape[0], sim_df_copy.shape[0])
        smooth_x = np.linspace(0, sim_df_copy.shape[0], 3)

        fig, ax = plt.subplots()

        plt.plot(sim_df, alpha = 0.05)
        ax.plot(smooth_x, interp1d(x, sim_df_copy['percentile_0'], kind='cubic')(smooth_x), alpha = 0)
        ax.plot(smooth_x, interp1d(x, sim_df_copy['percentile_1'], kind = 'cubic')(smooth_x), alpha = 0)
        ax.plot(smooth_x, interp1d(x, sim_df_copy['percentile_2'], kind = 'cubic')(smooth_x), alpha = 0)
        ax.plot(smooth_x, interp1d(x, sim_df_copy['percentile_3'], kind = 'cubic')(smooth_x), alpha = 0)
        ax.plot(smooth_x, interp1d(x, sim_df_copy['median'], kind = 'cubic')(smooth_x), alpha = 1, color = 'k', label = 'Median')
        ax.axhline(y = investment_amount, color = 'r', alpha = 0.4, linestyle = '--')

        ax.fill_between(smooth_x, interp1d(x, sim_df_copy['percentile_0'], kind='cubic')(smooth_x), interp1d(x, sim_df_copy['percentile_3'], kind = 'cubic')(smooth_x), alpha = 0.2, label = '95% CI')
        ax.fill_between(smooth_x, interp1d(x, sim_df_copy['percentile_1'], kind = 'cubic')(smooth_x), interp1d(x, sim_df_copy['percentile_2'], kind = 'cubic')(smooth_x), alpha = 0.4, label = '50% CI')
        plt.legend()
        plt.title('Monte Carlo simulation with confidence intervals')
        plt.xlabel('Time (days)')
        plt.ylabel('Portfolio value')
    
    return sim_df

def mc_sim_comparison(df, df2, weight_1, weight_2, timeframe, nsims, investment_amount = 1):
    # This function compares two different simulations
    # Show first simulation
    plt.figure()
    df_1 = mc_sim(df, weight_1, timeframe, nsims, investment_amount)
    plt.title('Portfolio 1')
    # Show second simulation
    plt.figure()
    df_2 = mc_sim(df2, weight_2, timeframe, nsims, investment_amount)
    plt.title('Portfolio 2')
    # Show the KDE plots of each simulations of their ending days together
    plt.figure()
    sns.kdeplot(df_1.iloc[-1,:], shade = True, alpha = 0.1, label = 'Portfolio 1')
    sns.kdeplot(df_2.iloc[-1,:], shade = True, alpha = 0.1, label = 'Portfolio 2')
    plt.title('Comparison of KDE plots for each portfolio')
    plt.legend()

def actual_return_plot(df, weight_list, timeframe, investment_amount = 1):
    # Using the dataframe, fetch the stock list data
    stock_list = df.columns.tolist()
    # Since we are finding actual returns of our potfolio afterwards, start date will be the last date of the original dataframe
    start_date = df.index[-1]
    end_date = start_date + dt.timedelta(timeframe)
    # Input dates are in string format so converting datetime types to string types
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    # Get the actual stock data for the future dates, find portfolio returns, and plot it
    new_df = fetch_stock_data(start_date, end_date, stock_list)
    daily_returns = new_df.pct_change().dropna()
    port_daily = np.cumprod(daily_returns.dot(weight_list) + 1) * investment_amount
    port_daily = port_daily.reset_index().drop(['timestamp'], axis = 1)
    plt.plot(port_daily, label = 'Actual return', linewidth = 1.5, color = 'lime')
    plt.legend()

